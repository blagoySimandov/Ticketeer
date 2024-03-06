from wtforms import DateField, DecimalField, FileField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired,NumberRange
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
class SearchForm(FlaskForm):
    search = StringField('Search')
    order= SelectField('Order by',choices=['Price Ascending','Price Descending',"Soonest","Latest"])
    type= SelectField('Type',
                      choices=['General','VIP'])
    submit = SubmitField()