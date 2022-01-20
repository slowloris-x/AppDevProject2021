from datetime import datetime
from constants import date_format, datetime_format


class Inventory:
    temp_dict = {
        '': 'Select', 'H': 'Hot', 'C': 'Cold'
    }
    cuisine_dict = {
        'C': 'Chinese', 'M': 'Malay', 'I': 'Indian', 'O': 'Others'
    }

    status_active = 1
    status_deleted = 0

    def __init__(self, cuisine, temp, name, price, profile_pic=None):
        self.profile_pic = profile_pic
        self.cuisine = cuisine
        self.temp = temp
        self.name = name
        self.time_created = datetime.now()
        self.time_updated = datetime.now()
        self.price = price
        self.status = Inventory.status_active
        self.id = name.replace(" ",'')

    def get_cuisine(self):
        return Inventory.cuisine_dict[self.cuisine]

    def get_price(self):
        return self.price

    def get_temp(self):
        return Inventory.temp_dict[self.temp]

    def get_name(self):
        return self.name

    def get_image(self):
        return self.profile_pic

    def __str__(self):
        return f'Temp:{self.temp}, ' \
               f'Cuisine:{self.cuisine}, ' \
               f'name:{self.name},' \
               f'name:{self.id}'
