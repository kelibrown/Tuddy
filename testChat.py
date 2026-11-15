from ChatSession import ChatSession

# create a test chat session
chat = ChatSession("session001", "user001")

# append or add messages
chat.appendMessage("user", "What are partial derivatives?")


chat.appendMessage(
    "assistant",
    "They measure how a function changes with respect to one variable."
)

# Display conversation history
print(chat.getFormattedHistory())
