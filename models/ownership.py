import uuid
class Ownership:
    __tablename__ = 'ownership'
    def __init__(self, user_id:str, ticket_id:str,id=uuid.uuid4()):
        self.id = id
        self.user_id = user_id
        self.ticket_id = ticket_id

    def __repr__(self):
        return f"Ownership(id='{self.id}', user_id='{self.user_id}', ticket_id='{self.ticket_id}')"
    def insert_ownership_instance(self,db):
        db.execute("""INSERT INTO ownership (id,user_id,ticket_id) VALUES(?,?,?)""",(str(self.id),self.user_id,self.ticket_id))
        