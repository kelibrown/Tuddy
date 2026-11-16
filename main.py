# import external classes being used

from dotenv import load_dotenv # file where API key is being securely stored
from openai import OpenAI


load_dotenv() # load .env file in

client = OpenAI()

try:
    response = client.responses.create(
        model = "gpt-6-luna",
        input = "You are Tuddy, an AI tutor, Introduce yourself in one sentence."
    )

    print(response.output_text)

except Exception as error:
    print("something went wrong:")
    print(type(error).__name__)
    print(error)