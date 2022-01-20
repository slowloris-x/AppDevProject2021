# Note: Use wtforms v3.0.0
from wtforms import Form, StringField, PasswordField, RadioField, SelectField, TextAreaField, EmailField, DateField, \
    validators, ValidationError, FileField, IntegerField
from wtforms.validators import NumberRange

from inventory import Inventory


class CreateInventoryForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    temp = SelectField('Temp', [validators.DataRequired()] ,choices=Inventory.temp_dict.items(), default='')
    cuisine = RadioField('Cuisine',choices=Inventory.cuisine_dict.items(), default='H')
    ProfileImage = FileField('Profile')
    price = IntegerField('Price',[validators.DataRequired(),NumberRange(min=0)],default=0)
