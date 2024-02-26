from datetime import datetime
import uuid


class User:
    def __init__(self, email, password_hash, first_name, last_name,id=uuid.uuid4(), bio=None, profile_picture=None,
                 phone_number=None, location=None, social_media_links=None, preferred_payment_methods=None,
                 notification_preferences=None, ticket_preferences=None, ticket_resale_history=None,
                 trustworthiness_indicators=None, security_settings=None, privacy_settings=None,
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
        self.preferred_payment_methods = preferred_payment_methods
        self.notification_preferences = notification_preferences
        self.ticket_preferences = ticket_preferences
        self.ticket_resale_history = ticket_resale_history
        self.trustworthiness_indicators = trustworthiness_indicators
        self.security_settings = security_settings
        self.privacy_settings = privacy_settings
        self.member_since = member_since if member_since is not None else datetime.now()
    def register_user(self, db)->(int):
        db.execute("INSERT INTO users (id,email, password_hash, first_name, last_name, member_since) VALUES (?,?,?,?,?,?) RETURNING id",
                   (str(self.id),self.email, self.password_hash, self.first_name, self.last_name,None)).fetchone()#passing none to memembersince makes it get the datetime.Now