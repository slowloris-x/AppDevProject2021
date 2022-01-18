from datetime import datetime
from constants import date_format, datetime_format


class Inventory:
    temp_dict = {
        '': 'Select', 'H': 'Hot', 'C': 'Cold'
    }
    cuisine_dict = {
        'C': 'Chinese', 'M': 'Malay', 'I': 'Indian', 'O': 'Others'
    }

    def __init__(self, cuisine, temp, name):
        self.cuisine = cuisine
        self.temp = temp
        self.name = name
        self.time_created = datetime.now()
        self.time_updated = datetime.now()

    def get_cuisine(self):
        return Inventory.cuisine_dict[self.cuisine]

    def get_temp(self):
        return Inventory.temp_dict[self.temp]

    def get_name(self):
        return self.name

    def __str__(self):
        return f'Temp:{self.temp}, ' \
               f'Cuisine:{self.cuisine}, '\
               f'name:{self.name}'
