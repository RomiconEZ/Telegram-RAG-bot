def dialog_router(human_input: str, user: dict, client, vector_db):
    print("vector_db")
    print(vector_db)
    print("client")
    print(client)
    some_context = ""
    try:
        search_results = vector_db.similarity_search(human_input, k=1)
        for result in search_results:
            some_context += result.page_content + "\n\n"
    except Exception:
        pass

    user['history'].append({"role": "user", "content": some_context + human_input})

    new_message = {"role": "assistant", "content": ""}

    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=user['history'],
        temperature=0.7,
        stream=True,
    )
    print("completion")
    print(completion)

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    # try:
    #     completion = client.chat.completions.create(
    #         model="local-model",  # this field is currently unused
    #         messages=user['history'],
    #         temperature=0.7,
    #         stream=True,
    #     )
    #     print("completion")
    #     print(completion)
    #
    #     for chunk in completion:
    #         if chunk.choices[0].delta.content:
    #             print(chunk.choices[0].delta.content, end="", flush=True)
    #             new_message["content"] += chunk.choices[0].delta.content
    # except Exception:
    #     new_message["content"] = 'Error'

    user['history'].append(new_message)

    return new_message["content"]
