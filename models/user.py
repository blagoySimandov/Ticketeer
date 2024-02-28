from datetime import datetime
import uuid


class User:
    def __init__(self, email, password_hash, first_name, last_name,id=uuid.uuid4(), bio=None, profile_picture=None,
                 phone_number=None, location=None, social_media_links=None,
                 notification_preferences=None, ticket_preferences=None,
                 trustworthiness_indicators=None,
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
        self.social_media_links = social_media_links
        self.notification_preferences = notification_preferences
        self.ticket_preferences = ticket_preferences
        self.trustworthiness_indicators = trustworthiness_indicators
        self.member_since = member_since if member_since is not None else datetime.now()
    @classmethod
    def from_db(cls, db, user_id):
        user_map = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
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
            social_media_links=user_map["social_media_links"],
            notification_preferences=user_map["notification_preferences"],
            ticket_preferences=user_map["ticket_preferences"],
            trustworthiness_indicators=user_map["trustworthiness_indicators"],
            member_since=user_map["member_since"]
        )
    def register_user(self, db)->(int):
        db.execute("INSERT INTO users (id,email, password_hash, first_name, last_name, member_since) VALUES (?,?,?,?,?,?) RETURNING id",
                   (str(self.id),self.email, self.password_hash, self.first_name, self.last_name,None)).fetchone()#passing none to memembersince makes it get the datetime.Now
