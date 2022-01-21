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
from inventory_form import CreateInventoryForm, CreateReviewForm, UpdateInventoryForm
from inventory import Inventory

db_inventory_key = "stock"
db_name = 'inventory'

db_review_key = 'review'


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
            if form.name.data.upper() in inventorylist:
                error = 'this name has been used before'
                return render_template('addInventory.html', form=form, error=error)
        else:
            name = form.name.data.upper()
            temperature = form.temp.data
            cuisine = form.cuisine.data
            price = form.price.data
            stock = form.stock.data

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

            finished_food = Inventory(cuisine, temperature, name, price, stock, filename)
            save_inventory(finished_food)
            print(finished_food)
            return redirect('/')
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


@inventory_controller.route('/foodpage/<foodname>', methods=['POST', 'GET'])
def add_review(foodname):
    form = CreateReviewForm(request.form)
    if request.method == 'POST':
        name = session.get('user_name')
        comment = form.message.data
        save_review(name,foodname,comment)
    review = get_review_list(foodname)
    count = len(review)
    food = get_inventory(foodname)
    return render_template('foodpage.html', food=food, review=review, form=form, count=count)


@inventory_controller.route('/deletePost/<userid>/<foodid>', methods=['POST', 'GET'])
def delete_post(userid,foodid):
    db = shelve.open('reviews','c')
    if 'allreviews' not in db:
        db['allreviews'] = {}
    cartdb = db['allreviews']
    if userid not in cartdb:
        cartdb[userid] = {}
    cartdb[foodid].pop(userid)
    db['allreviews'] = cartdb
    db.close()
    print('im fucking running')
    return redirect('/foodpage/'+foodid)



@inventory_controller.route('/updateInventory/<id>', methods=['POST', 'GET'])
def updateInventory(id):
    form = UpdateInventoryForm(request.form)
    if request.method == 'POST' and form.validate():
        inventory = get_inventory(id)
        temperature = form.temp.data
        cuisine = form.cuisine.data
        name = form.name.data
        stock = form.stock.data
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

        finished_food = Inventory(cuisine, temperature, name, price, stock, filename)
        save_inventory(finished_food)
        print(finished_food)

        return redirect(url_for('inventory.retrieve_inventory', id=inventory.id))
    else:
        inventory = get_inventory(id)

        form.temp.data = inventory.temp
        form.cuisine.data = inventory.cuisine
        form.name.data = inventory.name
        form.stock.data = inventory.stock
        form.price.data = inventory.price

    return render_template('/updateInventory.html', form=form)


@inventory_controller.route('/addtocart/<userid>/<foodid>')


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
        getinventory = stock[key].replace(" ", '')
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
    user_list2 = []
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


def save_review(userid,foodid, comment):
    db = shelve.open('reviews','c')
    if 'allreviews' not in db:
        db['allreviews'] = {}
    cartdb = db['allreviews']
    if userid not in cartdb:
        cartdb[userid] = {}
    cart= cartdb[userid]
    cart[foodid] = comment
    db['allreviews'] = cartdb
    db.close()


def get_review_list(foodid):
    db = shelve.open('reviews','c')
    if 'allreviews' not in db:
        db['allreviews'] = {}
    cartdb = db['allreviews']
    foodid_reviews = {}
    for userkey, user_reviews in cartdb.items():
      for key, comment in user_reviews.items():
        if key == foodid:
          foodid_reviews[userkey] = comment
    db.close()
    return foodid_reviews

def add_item_to_id_cart(foodid,userid):
    db = shelve.open('inventory','c')
    if 'allcart' not in db:
        db['allcart'] = {}
    cartdb = db['allcart']
    if userid not in cartdb:
        cartdb[userid] = {}
    cart= cartdb[userid]
    cart[foodid] = cart.get(foodid, 0) + 1
    db['cart'] = cartdb
    db.close()

def delete_item_cart(foodid,userid):
    db = shelve.open('inventory','c')
    if 'allcart' not in db:
        db['allcart'] = {}
    cartdb = db['allcart']
    if userid not in cartdb:
        cartdb[userid] = {}
    cart= cartdb[userid]
    cart[foodid] = cart.get(foodid, 0) - 1
    db['cart'] = cartdb
    db.close()

def show_cart(userid):
    db = shelve.open('inventory','c')
    if 'allcart' not in db:
        db['allcart'] = {}
    cartdb = db['allcart']
    if userid not in cartdb:
        cartdb[userid] = {}
    db.close()
    cart= cartdb[userid]
    return cart
