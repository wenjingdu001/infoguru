import chainlit as cl
from scripts.query_data import query_rag

@cl.on_chat_start
def start():
    cl.user_session.set("history", [])
    print("Chat session started and history initialized.")

@cl.on_message
async def main(message: cl.Message):

    history = cl.user_session.get("history")
    query_text = message.content

    processing_message = cl.Message(
        content="Processing your query..."
    )
    await processing_message.send()

    try:        
        # Call query_rag and log the result
        result = await cl.make_async(query_rag)(query_text)
        history.append((query_text, result))
    except Exception as e:
        response = f"An error occurred: {e}"
    await processing_message.remove()

    final_message = cl.Message(content=f"Response: {result['response']}\n\n---\n\nSources: {result['source']}")
    await final_message.send()

if __name__ == "__main__":
    cl.run()
    print("Chainlit application running.")
