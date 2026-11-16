from ChatSession import ChatSession
from AiTutorEngine import AiTutorEngine
from UserInterface import UserInterface


def main():

    chat_session = ChatSession()

    ai_tutor = AiTutorEngine()

    user_interface = UserInterface(
        ai_tutor,
        chat_session
    )

    user_interface.launch()


if __name__ == "__main__":
    main()