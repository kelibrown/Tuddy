
from openai import OpenAI


class AiTutorEngine:
    def __init__(self):
        self.client = OpenAI()

        self.current_model_version = "gpt-5.5"

        # remind Tuddy of its context with each prompt. define guidelines of how model should behave each time.
        self.socratic_prompt_template = """
        You are Tuddy, an academic AI assistant.

        Your goal is to help students learn and understand
        concepts rather than simply giving them answers.

        Encourage curiosity and critical thinking.
        Guide students through problems step by step.
        Ask guiding questions when appropriate.
        """

    def generate_socratic_response(self, student_question, chat_session):

        prompt = [
            {
                "role": "developer",
                "content": self.socratic_prompt_template
            }
        ]

        prompt.extend(chat_session.get_formatted_history())

        response = self.client.responses.create(
            model=self.current_model_version,
            input=prompt
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
