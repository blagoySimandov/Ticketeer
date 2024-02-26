from flask_wtf import FlaskForm
from wtforms import EmailField,StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired,Email,EqualTo

class SignUpForm(FlaskForm):
    f_name = StringField("First Name",validators=[InputRequired("First name is required.")])
    l_name = StringField("Last Name",validators=[InputRequired("Last name is required.")])
    email = EmailField('Email address', validators=[InputRequired("Email is required."), Email()])
    password = PasswordField("Password",validators=[InputRequired("Password is required.")])
    confirm_password = PasswordField("Confirm Password", [EqualTo("password","Your passwords do not match.")])
    submit = SubmitField("Sign up")
class LogInForm(FlaskForm):
    email = EmailField('Email address', validators=[InputRequired("Email is required."), Email()])
    password = PasswordField("Password",validators=[InputRequired("Password is required.")])
    submit = SubmitField("Log in")

