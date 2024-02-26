from datetime import datetime
from enum import Enum
import uuid
class ActionType(Enum):
    REGISTER = "Registered"
    POST_TICKET = "Posted a ticket"
    BUY_TICKET = "Bought a ticket"

class History:
    def __init__(self, user_id, action,id=uuid.uuid4(), timestamp=None, details=None):
        if timestamp is None:
            timestamp = datetime.now()
        if not isinstance(action, ActionType):
            raise ValueError("Invalid action type. Must be a member of ActionType enum.")
        self.id = id
        self.timestamp = timestamp
        self.user_id = user_id
        self.action = action
        self.details = details
    def insert_entry(self, db):
        db.execute("INSERT INTO history (id,timestamp, user_id, action, details) VALUES (?, ?, ?, ?, ?)",
                    (str(self.id),self.timestamp, str(self.user_id), self.action.value, self.details))