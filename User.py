from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4


def __init__(self, name, email, user_id: Optional[UUID] = None, account_creation_date: Optional[datetime] = None,
        preferred_language = "Eng", accessibility_mode: bool = False,):

        self.userID: UUID = user_id if user_id is not None else uuid4()
        self.name: str = name
        self.email: str = email
        self.accountCreationDate: datetime = (
            account_creation_date if account_creation_date is not None else datetime.now()
        )
        self.preferredLanguage: str = preferred_language
        self.accessibilityMode: bool = accessibility_mode

        # Internal lists to store user's documents and sessions
        self._documents: List[Document] = []
        self._sessions: List[StudySession] = []



def updatePreferences(self, language: str, accessibilityMode: bool) -> None:
    self.preferredLanguage = language
    self.accessibilityMode = accessibilityMode

def getUploadedDocuments(self)  -> List[Document]:
    return self._document

def getActivitySessions(self) -> List[StudySession]:
    return self._sessions

def verifyEmail(self) -> bool:
    return "@" in self.email and "." in self.email.split("@")[-1]
