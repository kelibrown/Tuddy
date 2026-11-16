
class ChatSession:
    def __init__(self):
        self.message_log = []

    def append_message(self, sender, text):
        message = {
            "role": sender,
            "content": text
        }
        self.message_log.append(message)

    def get_formatted_history(self):
        return self.message_log

    def clear_history(self):
        self.message_log = []