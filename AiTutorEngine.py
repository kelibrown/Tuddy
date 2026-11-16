# approached some errors with camel case and snake case confusion. modified all to be snake to keep private naming convention
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# CLASS 3: Document (Entity)
@dataclass
class Document:
    file_name: str
    extracted_text: str


# CLASS 7: StudyMaterial (Entity)
@dataclass
class StudyMaterial:
    material_type: str
    content: str


# DEMO STUDY DOCUMENT
study_document = Document(
    file_name="Biology_Notes.txt",
    extracted_text=(
        "Cellular respiration is the process by "
        "which cells convert nutrients into ATP. "
        "Glycolysis occurs in the cytoplasm and "
        "converts glucose into two pyruvate molecules. "
        "The citric acid cycle takes place in the "
        "mitochondrial matrix and produces NADH "
        "and FADH2. The electron transport chain "
        "is located in the inner mitochondrial "
        "membrane. Electrons from NADH and FADH2 "
        "move through protein complexes, helping "
        "create a proton gradient. ATP synthase "
        "uses this gradient to produce ATP. "
        "Oxygen acts as the final electron acceptor "
        "and is reduced to water."
    )
)


# CLASS 5: AITutorEngine (Control)
class AITutorEngine:

    def __init__(self, study_document):
        self._client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )
        self._current_model_version = "gpt-6-luna"
        self.study_document = study_document

        self._socratic_prompt_template = (
            "You are Tuddy, an educational AI tutor. "
            "Your purpose is to encourage learning, "
            "critical thinking, and independent reasoning."
        )

    # Private method: constructs the AI prompt
    def _construct_prompt(self, base_prompt, context, history):
        return (
            f"{base_prompt}\n\n"
            f"STUDY MATERIAL:\n{context}\n\n"
            f"ADDITIONAL CONTEXT:\n{history}"
        )

    # Private method: calls the OpenAI API
    def _execute_model_call(self, payload):
        response = self._client.responses.create(
            model=self._current_model_version,
            instructions=self._socratic_prompt_template,
            input=payload
        )

        if not response.output_text:
            raise ValueError("The AI returned no quiz text.")

        return response.output_text

    def generate_socratic_response(self, chat_session):
        response = self._client.responses.create(
            model=self._current_model_version,
            instructions=self._socratic_prompt_template,
            input=chat_session.get_formatted_history()
        )

        return response.output_text

    # Public method: generates a quiz
    def generate_quiz(self, topic):

        # Edit - modify instructions so that answer key isn't given right away
        quiz_instructions = (
            f"Generate exactly 5 multiple-choice "
            f"questions about {topic}.\n"
            "Use only the study material provided.\n"
            "Each question must have four options: "
            "A, B, C, and D.\n"
            "Include one correct answer per question, "
            "do NOT include the answers until the user provides answers.\n"
            "If the user does not provide answers and requests the answers,"
            "Provide them with extra motivation and context for the given question.\n"
            "After all questions are answered, or user is completely lost, include a separate "
            "answer key with short explanations.\n"
            "Make the quiz appropriate for a college student.\n"
            "If there is insufficient source information, "
            "say so instead of inventing facts."
        )

        prompt = self._construct_prompt(
            quiz_instructions,
            self.study_document.extracted_text,
            ""
        )

        generated_text = self._execute_model_call(prompt)

        return StudyMaterial(
            material_type="QUIZ",
            content=generated_text
        )
