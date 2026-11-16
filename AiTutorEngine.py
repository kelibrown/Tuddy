
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# CLASS 3: Document (Entity)
@dataclass
class Document:
    fileName: str
    extractedText: str


# CLASS 7: StudyMaterial (Entity)
@dataclass
class StudyMaterial:
    materialType: str
    content: str


# DEMO STUDY DOCUMENT
studyDocument = Document(
    fileName="Biology_Notes.txt",
    extractedText=(
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

    def __init__(self, studyDocument):
        self._client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )
        self._currentModelVersion = "gpt-6-luna"
        self.studyDocument = studyDocument

        self._socraticPromptTemplate = (
            "You are Tuddy, an educational AI tutor. "
            "Your purpose is to encourage learning, "
            "critical thinking, and independent reasoning."
        )

    # Private method: constructs the AI prompt
    def _constructPrompt(self, basePrompt, context, history):
        return (
            f"{basePrompt}\n\n"
            f"STUDY MATERIAL:\n{context}\n\n"
            f"ADDITIONAL CONTEXT:\n{history}"
        )

    # Private method: calls the OpenAI API
    def _executeModelCall(self, payload):
        response = self._client.responses.create(
            model=self._currentModelVersion,
            instructions=self._socraticPromptTemplate,
            input=payload
        )

        if not response.output_text:
            raise ValueError("The AI returned no quiz text.")

        return response.output_text

    def generate_socratic_response(self, chat_session):
        response = self._client.responses.create(
            model=self.current_model_version,
            instructions=self.socratic_prompt_template,
            input=chat_session.get_formatted_history()
        )

        return response.output_text

    # Public method: generates a quiz
    def generateQuiz(self, topic):

        quizInstructions = (
            f"Generate exactly 5 multiple-choice "
            f"questions about {topic}.\n"
            "Use only the study material provided.\n"
            "Each question must have four options: "
            "A, B, C, and D.\n"
            "Include one correct answer per question.\n"
            "After all questions, include a separate "
            "answer key with short explanations.\n"
            "Make the quiz appropriate for a college student.\n"
            "If there is insufficient source information, "
            "say so instead of inventing facts."
        )

        prompt = self._constructPrompt(
            quizInstructions,
            self.studyDocument.extractedText,
            ""
        )

        generatedText = self._executeModelCall(prompt)

        return StudyMaterial(
            materialType="QUIZ",
            content=generatedText
        )
