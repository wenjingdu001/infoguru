import chainlit as cl
from scripts.query_data import query_rag

def create_app():
    app = cl.Chainlit(__name__)

    @app.on_start
    def setup():
        pass

    @app.on_message
    async def handle_message(message: cl.Message):
        query_text = message.content
        if query_text:
            try:
                response = query_rag(query_text)
                await message.send(response)
            except Exception as e:
                await message.send(f"An error occurred: {e}")
        else:
            await message.send("Please enter a query")

    return app