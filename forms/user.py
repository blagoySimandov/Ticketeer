from wtforms import SelectField, StringField, TextAreaField, SubmitField, FormField, FieldList
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

class SocialForm(FlaskForm):
    social_media_platform = SelectField('Social Media Platform', choices=[
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
    ])
    add = SubmitField("Add")

class SocialLink(FlaskForm):
    link = StringField('Social Link')
    remove = SubmitField("Remove")


class UpdateUserForm(FlaskForm):
    bio = TextAreaField('Bio')
    profile_picture = FileField('Profile Picture')
    phone_number = StringField('Phone Number')
    location = StringField('Location')
    facebook = StringField('Facebook Link', )
    twitter = StringField('Twitter Link', )
    instagram = StringField('Instagram Link', )
    notification_preferences = StringField('Notification Preferences')
    ticket_preferences = StringField('Ticket Preferences')
    trustworthiness_indicators = StringField('Trustworthiness Indicators')
    social_media_platform = FormField(SocialForm)
    social_link = FieldList(FormField(SocialLink), min_entries=0,max_entries=3)
    save = SubmitField("Save changes")
