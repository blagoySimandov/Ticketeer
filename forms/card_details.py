from datetime import datetime,date
from wtforms import StringField, SubmitField, ValidationError,PasswordField
from wtforms.validators import DataRequired,Regexp,Length
from flask_wtf import FlaskForm
class CardDetails(FlaskForm):
    name = StringField("Cardholder's Name")
    number = StringField("Card Number",validators=[Length(message="Credit card number must be exactly 19 characters long.",min=19,max=19)])#1234 5678 9012 3457
    expr = StringField("Expiration",validators=[DataRequired(message="Expiration is required."),Length(message="",min=7,max=7)]) #MM/YYYY
    cvv =  PasswordField("CVV",validators=[Length(message=None,min=3,max=3),Regexp(message="CVV must be only numbers",regex=r'[0-9]{3}')])
    submit = SubmitField("Checkout")
    def validate_expr(form, field):
        try:
            expr_date = datetime.strptime(field.data, '%m/%Y').date()
        except ValueError:
            raise ValidationError("Invalid date format. Please use MM/YYYY.")
        if expr_date < date.today():
                raise ValidationError("Expiration date cannot be in the past.")