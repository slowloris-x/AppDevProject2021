# Note: Use wtforms v3.0.0
from wtforms import Form, StringField, PasswordField, RadioField, SelectField, TextAreaField, EmailField, DateField, \
    validators, ValidationError
from inventory import Inventory


class CreateInventoryForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    temp = SelectField('Temp', [validators.DataRequired()] ,choices=Inventory.temp_dict.items(), default='')
    cuisine = RadioField('Cuisine',choices=Inventory.cuisine_dict.items(), default='H')
