from openai import OpenAI
# gives us the ability to read variables from .env files
import os
from dotenv import load_dotenv
#
from openai import OpenAI




class AiTutorEngine:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPEN_API_KEY was not found in .env")

        self.client = OpenAI()


        self.current_model_version = "gpt-6-luna"

        # remind Tuddy of its context with each prompt. define guidelines of how model should behave each time.
        self.socratic_prompt_template = """
        You are Tuddy, an academic AI assistant.

        Your goal is to help students learn and understand
        concepts rather than simply giving them answers.

        Encourage curiosity and critical thinking.
        Guide students through problems step by step.
        Ask guiding questions when appropriate.
        """

    def generate_socratic_response(self, chat_session):
        response = self.client.responses.create(
            model=self.current_model_version,
            instructions=self.socratic_prompt_template,
            input=chat_session.get_formatted_history()
        )

        return response.output_text

    def generate_quiz(self, topic, question_count):

        prompt = f"""
        Create a {question_count}-question quiz about {topic}.

        Include multiple-choice questions and provide
        the correct answers separately at the end.
        """


        response = self.client.responses.create(
            model=self.current_model_version,
            input=prompt
        )

        return response.output_text
