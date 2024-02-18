import os
from pathlib import Path

from telegram import __version__ as TG_VER

from ai_agent import dialog_router

from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

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
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ['TG_BOT_TOKEN']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf'''
        Здравствуйте! Спасибо что выбрали нашу Турфирму! 
        Я ваш личный ассистент и с удовольствием помогу вам узнать информацию о нас.
        ''',
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    response = [
        '''
        Вы можете узнать адрес, номер телефона, e-mail и сайт нашего турагенства,
        если спросите это у ассистента.
        '''
    ]
    for i in response:
        await update.message.reply_text(i)


async def bot_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global client
    global vector_db

    # Инициализация истории, если она еще не создана
    if 'history' not in context.user_data:
        context.user_data['history'] = [
            {"role": "system",
             "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both "
                        "correct"
                        "and helpful."}
        ]

    user_tg = update.effective_user
    user = {'user_id': user_tg.id, 'user_name': user_tg.username}
    bot_response = dialog_router(update.message.text, user, context, client, vector_db)
    await update.message.reply_text(bot_response)


def main() -> None:
    """Start the bot."""
    global vector_db
    global client

    current_path = Path(__file__).parent
    loaders = [PyPDFLoader(str(current_path / 'Document/Company_description.pdf'))]

    docs = []
    for file in loaders:
        docs.extend(file.load())
    # split text to chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(docs)
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                               model_kwargs={'device': 'cpu'})
    vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")

    client = OpenAI(base_url="http://host.docker.internal:1234/v1", api_key="not-needed")

    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_dialog))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
