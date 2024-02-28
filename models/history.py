from datetime import datetime
from enum import Enum
import uuid
class ActionType(Enum):
    REGISTER = "Registered"
    POST_TICKET = "Posted a ticket"
    BUY_TICKET = "Bought a ticket"

class History:
    def __init__(self, user_id, action,id=uuid.uuid4(), timestamp=None, details=None,ticket_id=None):
        if timestamp is None:
            timestamp = datetime.now()
        if not isinstance(action, ActionType):
            raise ValueError("Invalid action type. Must be a member of ActionType enum.")
        self.id = id
        self.timestamp = timestamp
        self.user_id = user_id
        self.action = action
        self.details = details
        self.ticket_id = ticket_id
    @classmethod
    def fetch_history(cls, db, user_id):
        history_records = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10;", (user_id,)).fetchall()
        history_list = []
        for record in history_records:
            action_enum = ActionType(record['action'])
            history_list.append(cls(
                id=record['id'],
                timestamp=record['timestamp'],
                user_id=record['user_id'],
                action=action_enum,
                details=record['details'],
                ticket_id=record['ticket_id']
            ))
        return history_list
    def insert_entry(self, db):
        db.execute("INSERT INTO history (id,timestamp, user_id, action, details,ticket_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (str(self.id),self.timestamp, str(self.user_id), self.action.value, self.details,str(self.ticket_id)))
        