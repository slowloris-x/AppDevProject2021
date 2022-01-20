from flask import Blueprint, render_template, request, redirect, session, url_for, send_file, send_from_directory
from user_forms import CreateUserForm, UpdateUserForm, LoginForm, changePassword
from user import User
from user_service import get_user_list, get_user, save_user, get_user_for_login, by_time_updated
from datetime import datetime
from constants import date_format, datetime_format
import os
from flask import Flask, flash, request, redirect, url_for, current_app

UPLOAD_FOLDER = 'assignment1/static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

db_users_key = 'stock'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@inventory_controller.route('/addInventory', methods=['GET', 'POST'])
def add_inventory():
    form = CreateInventoryForm(request.form)
    inventory = get_inventory_list()
    print(inventory)
    if request.method == 'POST' and form.validate():
        inventorylist = []
        for inventory in get_inventory_list():
            inventorylist.append(inventory.name)
            print(inventorylist)
            if form.name.data in inventorylist:
                error = 'this name has been used before'
                return render_template('addInventory.html', form=form, error=error)
        else:
            name = form.name.data
            temperature = form.temp.data
            cuisine = form.cuisine.data
            price = form.price.data

            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            print(file)

            filename = 'default'
            print(filename)
            if request.files['file'].filename != '':
                filename = request.form["name"]
                file.save(
                    os.path.join(os.path.dirname(current_app.instance_path),
                                 "static\\images", (filename + ".jpg")))

            finished_food = Inventory(cuisine, temperature, name, price, filename)
            save_inventory(finished_food)
            print(finished_food)
            return render_template('home.html')
    return render_template('addInventory.html', form=form)


@inventory_controller.route('/retrieveInventory')
def retrieve_inventory():
    inventory_list = get_inventory_list()
    return render_template('retrieveInventory.html', inventory_list=inventory_list)


@inventory_controller.route('/deleteFood/<food>', methods=['POST'])
def delete_food(food):
    fooddel = get_inventory(food)
    fooddel.status = Inventory.status_deleted
    save_inventory(fooddel)
    return redirect('/retrieveInventory')



# @inventory_controller.route("/sendimage/<img>")
# def send_img(img):
#     return send_file('static/images/' + img)



def get_inventory(key):
    stock = {}
    db = shelve.open(db_name)
    if db_inventory_key in db:
        stock = db[db_inventory_key]
    db.close()
    if key in stock:
        getinventory = stock[key]
        return getinventory

def get_inventory_nospace(key):
    stock = {}
    db = shelve.open(db_name)
    if db_inventory_key in db:
        stock = db[db_inventory_key]
    db.close()
    if key in stock:
        getinventory = stock[key].replace(" ",'')
        return getinventory



def get_inventory_list():
    user_dict = {}
    db = shelve.open(db_name)
    if db_inventory_key in db:
        user_dict = db[db_inventory_key]
    db.close()
    user_list = user_dict.values()
    user_list = filter(check_status, user_list)
    return user_list

def get_inventory_list_nospace():
    user_dict = {}
    user_list2 =[]
    db = shelve.open(db_name)
    if db_inventory_key in db:
        user_dict = db[db_inventory_key]
    db.close()
    user_list = user_dict.values()
    user_list = filter(check_status, user_list)
    for i in user_list:
        user_list = ''.join(i.get_name().split())
        user_list2.append(user_list)
    return user_list2



def check_status(user):
    return user.status > 0


def save_inventory(food):
    food.time_updated = datetime.now()
    inventory_dict = {}
    db = shelve.open(db_name)
    if db_inventory_key in db:
        inventory_dict = db[db_inventory_key]
    inventory_dict[food.name] = food
    db[db_inventory_key] = inventory_dict
    db.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


print(get_inventory('ice cream'))
