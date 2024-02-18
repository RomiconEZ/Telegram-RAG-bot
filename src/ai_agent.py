RAG_PROMPT = '''
Prompt:
1. Directly answer the user's query with a concise and accurate response, using the same language as the query without any additional explanatory text or process description.
2. When the query requires specific information or facts from the knowledge base, provide an accurate and relevant response in the query's language.
3. For general queries that do not require specific knowledge base data, give clear and direct advice or information based on general knowledge, ensuring the response is in the same language as the query.
4. The response should directly address the user's query with a focus on brevity and relevance, strictly maintaining language consistency.

Example user query: What is the area of France?
Response: The area of France is 643,801 square kilometers.

Example user query: Как мне улучшить игру в шахматы?
Response: Чтобы улучшить игру в шахматы, регулярно практикуйтесь, изучайте тактику и стратегии шахмат, а также анализируйте свои партии.

Example user query: Здравствуйте!
Response: Привет!

Data from the knowledge base:\n
'''


def dialog_router(human_input: str, user: dict, context, client, vector_db):
    global RAG_PROMPT
    some_context = RAG_PROMPT
    try:
        search_results = vector_db.similarity_search(human_input, k=1)
        for result in search_results:
            some_context += result.page_content + "\n"
    except Exception:
        pass

    context['history'].append({"role": "user", "content": some_context + "user's query: " + human_input})

    new_message = {"role": "assistant", "content": ""}

    try:
        completion = client.chat.completions.create(
            model="local-model",  # this field is currently unused
            messages=context['history'],
            temperature=0.2,
            stream=True,
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                new_message["content"] += chunk.choices[0].delta.content
    except Exception:
        new_message["content"] = 'Извините, в данный момент ассистент не доступен. Попробуйте обратиться позже.'
        context['history'] = []

    context['history'].append(new_message)

    # Храним только 4 последних сообщений в диалоге
    context['history'] = context['history'][-4:]

    return new_message["content"]
