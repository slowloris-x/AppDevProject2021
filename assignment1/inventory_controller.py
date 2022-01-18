from flask import Blueprint, render_template, request, redirect, session, url_for
from user_forms import CreateUserForm, UpdateUserForm, LoginForm, changePassword
from user import User
from user_service import get_user_list, get_user, save_user, get_user_for_login
from datetime import datetime
from constants import date_format, datetime_format

inventory_controller = Blueprint('inventory', __name__)
import shelve
from inventory_form import CreateInventoryForm
from inventory import Inventory

db_inventory_key = "stock"
db_name = 'inventory'


#
# @inventory_controller.route('/inventory')
# def Retrieve_inventory():
#
#
@inventory_controller.route('/addInventory',methods=['GET','POST'])
def add_inventory():
    form = CreateInventoryForm(request.form)
    inventory = get_inventory()
    print(inventory)
    if request.method == 'POST' and form.validate():
        inventorylist = []
        for inventory in get_inventory():
            inventorylist.append(inventory)
        print(inventorylist)
        if form.name == inventorylist:
            error = 'this name has been used before'
            return render_template('createUser.html', form=CreateInventoryForm, error=error)
        else:
            name = form.name.data
            temperature = form.temp.data
            cuisine = form.cuisine.data
            finished_food = Inventory(cuisine, temperature, name)
            save_inventory(finished_food)
            return render_template('retrieveFood.html')
    return render_template('addInventory.html',form=form)

def get_inventory(key):
    stock = {}
    db = shelve.open(db_name)
    if db_inventory_key in db:
        stock = db[db_inventory_key]
    db.close()
    if key in stock:
        getinventory = stock[key]
        return getinventory


def save_inventory(food):
    food.time_updated = datetime.now()
    inventory_dict = {}
    db = shelve.open(db_name)
    if db_inventory_key in db:
        inventory_dict = db[db_inventory_key]
    inventory_dict[food.name] = food
    db[db_inventory_key] = inventory_dict
    db.close()
