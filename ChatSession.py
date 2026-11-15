
class ChatSession:

    def __init__(self, session_id, user_id):
        self.sessionID = session_id
        self.userID = user_id

        self.startedAt = None
        self.lastActiveAt = None

        self.messageLog = []

    def appendMessage(self, sender, text):
        message = {
            "role": sender,
            "content": text
        }

        self.messageLog.append(message)

    def getFormattedHistory(self):
        return self.messageLog

    def clearHistory(self):
        self.messageLog.clear()
