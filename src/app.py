import os
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI
from telegram import __version__ as TG_VER

from ai_agent import dialog_router

vector_db = None
client = None

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.environ["TG_BOT_TOKEN"]
START_TEXT = """
Здравствуйте! Спасибо что выбрали нашу Турфирму! \nЯ ваш личный ассистент и с удовольствием помогу вам узнать информацию о нас.\n\n
/help - чтобы узнать о нас побольше\n
"""
HELP_TEXT = """
Вы можете узнать адрес, номер телефона, e-mail и сайт нашего турагенства, если спросите это у ассистента.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет приветственное сообщение при использовании команды /start.

    Args:
        update: Объект Update, содержащий информацию о текущем обновлении.
        context: Контекст, предоставляемый библиотекой для хранения данных между вызовами.
    """
    user = update.effective_user
    await update.message.reply_html(
        START_TEXT,  # START_TEXT должен быть предварительно определен с приветственным текстом
        reply_markup=ForceReply(
            selective=True
        ),  # Принудительный ответ только от получателя команды
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет сообщение с помощью при использовании команды /help.

    Args:
        update: Объект Update, содержащий информацию о текущем обновлении.
        context: Контекст, предоставляемый библиотекой для хранения данных между вызовами.
    """
    response = [
        HELP_TEXT  # HELP_TEXT должен быть предварительно определен с текстом помощи
    ]
    for i in response:
        await update.message.reply_text(i)


async def bot_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает диалог с пользователем, не связанный с командами.

    Args:
        update: Объект Update, содержащий информацию о текущем обновлении.
        context: Контекст, предоставляемый библиотекой для хранения данных между вызовами.
    """
    global client  # Использование глобального клиента API
    global vector_db  # Использование глобальной векторной базы данных

    # Инициализация истории диалога, если она еще не создана
    if "history" not in context.user_data:
        context.user_data["history"] = []

    user_tg = update.effective_user
    user = {
        "user_id": user_tg.id,
        "user_name": user_tg.username,
    }  # Словарь с данными пользователя
    bot_response = dialog_router(
        update.message.text, user, context.user_data, client, vector_db
    )
    await update.message.reply_text(bot_response)  # Ответ пользователю


def main() -> None:
    """
    Основная функция для запуска бота.
    """
    global vector_db  # Глобальная векторная база данных
    global client  # Глобальный клиент для API

    # Инициализация и загрузка документов
    current_path = Path(__file__).parent
    loaders = [PyPDFLoader(str(current_path / "Document/Company_description.pdf"))]

    docs = []
    for file in loaders:
        docs.extend(file.load())  # Загрузка текста из PDF-файлов

    # Разбиение текста на части
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(docs)

    # Создание векторного представления текста
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )
    vectorstore = Chroma.from_documents(
        docs, embedding_function, persist_directory="./chroma_db"
    )

    client = OpenAI(
        base_url="http://host.docker.internal:1234/v1", api_key="not-needed"
    )

    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_db = Chroma(
        persist_directory="./chroma_db", embedding_function=embedding_function
    )

    # Настройка и запуск бота
    application = (
        Application.builder().token(TOKEN).build()
    )  # TOKEN должен быть предварительно определен
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_dialog))
    application.run_polling()  # Запуск бота


if __name__ == "__main__":
    main()
