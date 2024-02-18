RAG_PROMPT = """
Prompt:
1. Directly answer the user's query with a concise and accurate response, using the same language as the query without any additional explanatory text or process description.
2. When the query requires specific information or facts from the knowledge base, provide an accurate and relevant response in the query's language.
3. For general queries that do not require specific knowledge base data, give clear and direct advice or information based on general knowledge, ensuring the response is in the same language as the query.
4. The response should directly address the user's query with a focus on brevity and relevance, strictly maintaining language consistency.
5. You don't have to give an explanation for the answer.
6. The answer should be in only one language. In the same language as the incoming question
7. You don't need to use the word 'Ответ' or 'Response' before the text

Example user query: What is the area of France?
Response: The area of France is 643,801 square kilometers.

Example user query: Как мне улучшить игру в шахматы?
Response: Чтобы улучшить игру в шахматы, регулярно практикуйтесь, изучайте тактику и стратегии шахмат, а также анализируйте свои партии.

Example user query: Здравствуйте!
Response: Привет!

Data from the knowledge base:\n
"""


def dialog_router(human_input: str, user: dict, context, client, vector_db):
    """
    Функция маршрутизации диалога для обработки пользовательского ввода и взаимодействия с векторной базой данных.

    Аргументы:
    human_input (str): Ввод от пользователя.
    user (dict): Словарь с информацией о пользователе.
    context: Контекст текущего диалога.
    client: Клиент для взаимодействия с внешним API или сервисом.
    vector_db: Векторная база данных для поиска похожих результатов.

    Описание работы функции:
    1. Использует глобальную переменную RAG_PROMPT как начальный контекст.
    2. Выполняет поиск в векторной базе данных для нахождения похожего контента на основе пользовательского ввода.
    3. Добавляет результаты поиска в контекст диалога.
    4. Строит и отправляет новое сообщение от ассистента, используя историю диалога.
    5. В случае ошибки возвращает сообщение об недоступности ассистента.
    6. Обновляет историю диалога, храня только последние 4 сообщения.
    """
    global RAG_PROMPT
    some_context = RAG_PROMPT  # Начальный контекст для диалога
    try:
        # Поиск похожего контента в векторной базе данных
        search_results = vector_db.similarity_search(human_input, k=1)
        for result in search_results:
            # Добавление содержания страницы в контекст
            some_context += result.page_content + "\n"
    except Exception:
        pass  # Игнорирование ошибок во время поиска

    # Добавление информации о запросе пользователя в историю диалога
    context["history"].append(
        {"role": "user", "content": some_context + "user's query: " + human_input}
    )

    new_message = {"role": "assistant", "content": ""}  # Новое сообщение от ассистента

    try:
        # Генерация ответа ассистента
        completion = client.chat.completions.create(
            model="local-model",  # Это поле в данный момент не используется
            messages=context["history"],
            temperature=0.2,
            stream=True,
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                # Вывод содержимого и добавление в сообщение ассистента
                print(chunk.choices[0].delta.content, end="", flush=True)
                new_message["content"] += chunk.choices[0].delta.content
    except Exception:
        # Обработка ошибок и уведомление пользователя
        new_message["content"] = (
            "Извините, в данный момент ассистент не доступен. Попробуйте обратиться позже."
        )
        context["history"] = []  # Очистка истории диалога

    # Добавление нового сообщения в историю
    context["history"].append(new_message)

    # Храним только 4 последних сообщения в диалоге
    context["history"] = context["history"][-4:]

    return new_message["content"]  # Возвращаем содержимое нового сообщения
