from flask import Blueprint, render_template, request, redirect, session, url_for
from user_forms import CreateUserForm, UpdateUserForm, LoginForm, changePassword
from user import User
from user_service import get_user_list, get_user, save_user, get_user_for_login, save_user_noupdate
from datetime import datetime
from constants import date_format, datetime_format

user_controller = Blueprint('user', __name__)


@user_controller.route('/retrieveUsers')
def retrieve_users():
    user_list = get_user_list()
    return render_template('retrieveUsers.html', count=len(user_list), user_list=user_list)


@user_controller.route('/createUser', methods=['GET', 'POST'])
def create_user():
    user_list = get_user_list()
    create_user_form = CreateUserForm(request.form)
    #     another way to validate
    # found = False
    # for user in user_list:
    #     if create_user_form.email.data == user.email:
    #         found = True
    # if found:
    #     error = "this email has been used before"
    #     return render_template('createUser.html', form=create_user_form, error=error)
    if request.method == 'POST' and create_user_form.validate():
        lollist = []
        for user in user_list:
            lollist.append(user.email)
        print(lollist)

        if create_user_form.email.data in lollist:
            error = "this email has been used before"
            return render_template('createUser.html', form=create_user_form, error=error)
        else:
            email = create_user_form.email.data
            password = create_user_form.password.data
            name = create_user_form.name.data
            gender = create_user_form.gender.data
            birthday = create_user_form.birthday.data
            user_type = create_user_form.user_type.data
            remarks = create_user_form.remarks.data
            user = User(email, password, name, gender, remarks, birthday, user_type)
            print(user)
            save_user(user)
            return redirect('/retrieveUsers')
    else:
        return render_template('createUser.html', form=create_user_form)


@user_controller.route('/updateUser/<id>', methods=['GET', 'POST'])
def update_user(id):
    user = get_user(id)
    update_user_form = UpdateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        user.email = update_user_form.email.data
        user.name = update_user_form.name.data
        user.gender = update_user_form.gender.data
        user.birthday = update_user_form.birthday.data
        user.user_type = update_user_form.user_type.data
        user.remarks = update_user_form.remarks.data
        print(user)
        save_user(user)
        return redirect('/retrieveUsers')
    else:
        update_user_form.email.data = user.email
        update_user_form.name.data = user.name
        update_user_form.gender.data = user.gender
        update_user_form.birthday.data = user.birthday
        update_user_form.user_type.data = user.user_type
        update_user_form.remarks.data = user.remarks
        return render_template('updateUser.html', form=update_user_form)


@user_controller.route('/deleteUser/<id>', methods=['POST'])
def delete_user(id):
    user = get_user(id)
    user.status = User.status_deleted
    save_user(user)
    return redirect('/retrieveUsers')


@user_controller.route('/deleteProfile/<id>', methods=['POST'])
def delete_profile(id):
    user = get_user(id)
    user.status = User.status_deleted
    save_user(user)
    session.clear()
    return redirect('/')


@user_controller.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data
        user = get_user_for_login(email, password)

        if user is not None:
            session['user_name'] = user.name
            session['user_type'] = user.user_type
            session['user_id'] = user.id
            user.time_login = datetime.now()
            print(f'last login:{user.time_login}')
            save_user_noupdate(user)
            return redirect('/')
        else:
            error = 'Invalid email or password'
            return render_template('login.html', form=login_form, error=error)
    else:
        return render_template('login.html', form=login_form)


@user_controller.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user_controller.route('/profile/<id>', methods=['GET', 'POST'])
def profile(id):
    user = get_user(id)
    return render_template('profile.html', user=user)


@user_controller.route('/profile/updateProfile', methods=['GET', 'POST'])
def updateProfile():
    if 'user_id' not in session:
        return redirect('/')

    form = UpdateUserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = get_user(session['user_id'])

        user.email = form.email.data
        user.name = form.name.data
        user.gender = form.gender.data
        user.remarks = form.remarks.data
        user.birthday = form.birthday.data
        user.user_type = form.user_type.data
        save_user(user)

        return redirect(url_for('user.profile', id=session['user_id']))
    else:
        user = get_user(session['user_id'])

        form.user_type.data = user.user_type
        form.email.data = user.email
        form.name.data = user.name
        form.gender.data = user.gender
        form.remarks.data = user.remarks
        form.birthday.data = user.birthday
        form.user_type.data = user.user_type

    return render_template('updateUser.html', form=form)


@user_controller.route('/changePassword', methods=['GET', 'POST'])
def changePass():
    if 'user_id' not in session:
        return redirect('/')

    form = changePassword(request.form)

    if request.method == 'POST' and form.validate():
        user = get_user(session['user_id'])

        user.password = form.new_password.data

        save_user(user)

        return redirect(url_for('user.profile', id=session['user_id']))
    return render_template('changePass.html', form=form)
