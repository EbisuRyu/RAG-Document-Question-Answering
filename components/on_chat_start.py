import chainlit as cl


welcome_message = """
Welcome to PDF QA! To get started:
**1. Upload a PDF or text file
2. Ask a question about the file**
"""


@cl.on_chat_start
async def on_chat_start():
    files = None
    while files is None:

        files = await cl.AskFileMessage(
            content=welcome_message,
            accept=["text/plain", "application/pdf"],
            max_size_mb=20,
            timeout=180
        ).send()

        file = files[0]
        msg = cl.Message(content=f"Processing '{file.name}'...")
        await msg.send()

        msg.content = f"'{file.name}' processed. You can now ask questions!"
        await msg.update()
