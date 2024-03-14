from wtforms import DateField, DecimalField, FileField, IntegerField, SelectField, StringField, TimeField, ValidationError
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm
from datetime import date,datetime
from flask_wtf.file import FileField, FileAllowed
class TicketForm(FlaskForm):
    eventName = StringField('Event Name', validators=[DataRequired()])
    eventDate = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    eventTime = TimeField('Event Time', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    ticketType = SelectField('Ticket Type', choices=[('VIP', 'VIP'), ('General', 'General')], validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    seatNumber = StringField('Seat Number/Section')
    ticketPDF = FileField('Upload Ticket (PDF)', validators=[DataRequired(),FileAllowed(["pdf","png","jpg"])])
    sellerPhone = StringField('Your Phone Number', validators=[DataRequired()])
    def validate_eventDate(form, field):
        if not field.data>=date.today():
            raise ValidationError("Event date cannot have already passed.")
    