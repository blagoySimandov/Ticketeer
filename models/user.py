from datetime import datetime
from ..models.ticket import Ticket
import uuid


class User:
    __tablename__ = 'users'
    def __init__(self, email, password_hash, first_name, last_name,id=uuid.uuid4(), bio=None, profile_picture=None,
                 phone_number=None, location=None, instagram='',facebook='',twitter='',owns=None,
                 member_since=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.profile_picture = profile_picture
        self.phone_number = phone_number
        self.location = location
        self.facebook = facebook
        self.twitter = twitter
        self.instagram = instagram
        self.member_since = member_since if member_since is not None else datetime.now()
        self.owns = owns
    @classmethod
    def from_db(cls, db, user_id):
        """  Create a User instance from the database.
            In the User object under the field 'owns' is stored an array of ticket objects
            that show which tikcets are owned by the user.

            Might be better to only hold the user ids instead of the whole objects.
            But since the scale of the application is small, perfomance concerncs will be dis-
            regarded for convenience
        """
        user_map = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        tickets_owned = db.execute("SELECT ticket_id FROM ownership where user_id=?",(user_id,)).fetchall() #fetches all the tickets owned by a user.
        ticket_ids = [x['ticket_id'] for x in tickets_owned]
        ownership = Ticket.fetch_tickets_by_ids(db,ticket_ids)#returns a list of tickets
        return cls(
            user_map["email"],
            user_map["password_hash"],
            user_map["first_name"],
            user_map["last_name"],
            id=user_map["id"],
            bio=user_map["bio"],
            profile_picture=user_map["profile_picture"],
            phone_number=user_map["phone_number"],
            location=user_map["location"],
            facebook=user_map["facebook"],
            twitter=user_map["twitter"],
            instagram=user_map["instagram"],
            member_since=user_map["member_since"],
            owns= ownership
        )
    #checks the form to see which fields are different and returns those fields in a map.
    def update_from_form(self,form, request):
        updated_fields = {}
        if self.bio != form.bio.data:
            self.bio = form.bio.data
            updated_fields['bio'] = form.bio.data
        if self.location != form.location.data:
            self.location = form.location.data
            updated_fields['location'] = form.location.data
        if self.profile_picture != None:
            updated_fields['profile_picture'] = self.profile_picture #already updated outside the function with the proper uuid file name.

        if self.phone_number != form.phone_number.data:
            self.phone_number = form.phone_number.data
            updated_fields['phone_number'] = form.phone_number.data

        if self.facebook != request.form.get('facebook', ""):
            self.facebook = request.form.get('facebook', "")
            updated_fields['facebook'] = self.facebook

        if self.twitter != request.form.get('twitter', ""):
            self.twitter = request.form.get('twitter', "")
            updated_fields['twitter'] = self.twitter

        if self.instagram != request.form.get('instagram', ""):
            self.instagram = request.form.get('instagram', "")
            updated_fields['instagram'] = self.instagram
        return updated_fields
    def update_to_db(self,db,updated_fields):
        if updated_fields:
            update_query = "UPDATE users SET "
            update_query += ", ".join([f"{key} = ?" for key in updated_fields.keys()])
            update_query += " WHERE id = ?"
            values = list(updated_fields.values()) + [self.id]
            db.execute(update_query, values)
    def register_user(self, db)->(int):
        db.execute("INSERT INTO users (id,email, password_hash, first_name, last_name, member_since) VALUES (?,?,?,?,?,?) RETURNING id",
                   (str(self.id),self.email, self.password_hash, self.first_name, self.last_name,None)).fetchone()#passing none to memembersince makes it get the datetime.Now
