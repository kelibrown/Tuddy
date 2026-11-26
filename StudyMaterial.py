from typing import List, Optional
from uuid import UUID, uuid4

def __init__(self, document_id: Optional[UUID], user_id: Optional[UUID], _content: str = None,):
        self.documentID: UUID = document_id if document_id is not None else uuid4()
        self.userID: UUID = user_id if user_id is not None else uuid4()
        self.answerKey: List[str] = []
        self.content: str = _content


def _createMaterial(self) -> None:
    self._content = self._content.strip()

def _setAnswerKey(self, answers: List[str]) -> List[str]:
    self._answerKey = answers
    return self._answerKey

def associateUser(self, user) -> None:
    self.userID = user.userID


def getDocument(userID: UUID, documentID: UUID) -> "Document":
    if userID._document is not None:
        if userID._document.documentID == documentID:
            return userID._document
    return None

def associateDocument(user, document) -> None:
        user._document = document
        user.documentID = document.documentID
