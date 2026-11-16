
from dotenv import load_dotenv

from AiTutorEngine import AITutorEngine, study_document
from ChatSession import ChatSession
from UserInterface import UserInterface

load_dotenv()


def main():
    chat_session = ChatSession()

    # Pass the existing study document into the AI engine
    ai_tutor = AITutorEngine(study_document)

    # Create and launch the interface
    user_interface = UserInterface(
        ai_tutor,
        chat_session
    )

    user_interface.launch()


if __name__ == "__main__":
    main()
