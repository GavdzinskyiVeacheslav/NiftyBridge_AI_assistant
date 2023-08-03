from fastapi import FastAPI, Header
from app import openai_answers

app = FastAPI()


@app.post('/api/send')
def send_question(message, x_api_key_token: str = Header(...)):
    """
        Endpoint for sending a message and receiving a response.

        Parameters:
        - message: The message to be sent (input)
        - x_api_key_token: API key token provided in the request header

        Returns:
        - response: The generated response message
    """
    if message:
        return {'message': openai_answers(message)}
