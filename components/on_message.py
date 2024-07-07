import chainlit as cl


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangChainCallBackHandler()

    res = await chain.ainvoke(message.content, callbacks=[cb])
    answer = "This is answer for your question:"
    source_documents = res["source_documents"]

    text_elements = []
    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]
        if source_names:
            answer += f"\nSource: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found!"

    await cl.Message(content=answer, elements=text_elements).send()
