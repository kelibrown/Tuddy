from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-6-luna", #ai model
        input="You are Tuddy, an AI tutor. Introduce yourself in one sentence."
    )

    print(response.output_text)

except Exception as error:
    print("Something went wrong:")
    print(type(error).__name__)
    print(error)