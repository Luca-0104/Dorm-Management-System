from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from wtforms import ValidationError

from . import auth
from .. import db
from ..main import main
from ..models import User
from flask_login import logout_user, login_required, login_user, current_user

get_role_from_button = True
role_id = None


# # Updates the last access time of the logged-in user
# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated:       # Determine whether the current user is logged in
#         current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    global get_role_from_button
    global role_id

    if request.method == 'POST':
        get_role_from_button = False
        stu_wor_id = request.form.get('stu_wor_id')     # 向前端索要学工号
        password = request.form.get('password')
        user = User.query.filter_by(stu_wor_id=stu_wor_id).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            return redirect(url_for('auth.home'))            # 少路由，指向home界面
        else:
            flash('Invalid id or password.')

    # decide if we need to get the role_id again
    if request.method == 'GET' and get_role_from_button is True:
        role_id = int(request.args.get('identification'))
        print(role_id)

    getf = request.args.get('f')
    if getf is not None:
        getf = int(getf)
    if getf == 1:
        return render_template('samples/phoneLogin.html', role_id=role_id)
    if getf == 2:
        return render_template('samples/emailLogin.html', role_id=role_id)
    return render_template('samples/login-2.html', role_id=role_id)


# Logout
@auth.route('/logout')
@login_required     # Make sure the user want to logout has logged in
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/sendMsg')
def send_message():
    pass


@auth.route('/home')
def home():
    return render_template('samples/homepage.html')


# register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    global get_role_from_button

    if request.method == 'POST':
        username = request.form.get('username')
        stu_wor_id = request.form.get('stu_wor_id')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # stu_wor_id = '19206'           # 即删
        if not all([username, stu_wor_id, email, phone, password, password2]):
            flash('elements are incomplete')
            print('elements are incomplete')

        elif password != password2:
            flash('Two passwords do not match')
            print('Two passwords do not match')

        else:
            print(validate_email(email))
            print(validate_phone(phone))
            print(validate_id(stu_wor_id))

            if validate_email(email) and validate_phone(phone) and validate_id(stu_wor_id): # 正式则启用
            # if validate_email(email) and validate_phone(phone):

                # 正式则启用
                # new_user = User(user_name=username, role_id=role_id,  password=password, email=email, stu_wor_id=stu_wor_id, phone=phone)
                new_user = User(user_name=username, stu_wor_id=stu_wor_id, role_id=role_id, password=password, email=email, phone=phone)
                flash('Registered successfully! You can login now.')
                db.session.add(new_user)
                db.session.commit()
                get_role_from_button = False    # we will go back to the login page and in this case we do not need to get the role_id again
                return redirect(url_for("auth.login"))
            else:
                flash('Email, phone number or id already exists.')
    return render_template('samples/register-2.html', role_id=role_id)


def validate_email(e):
    """
    Verify if the email has not been used.
    :param e:   email
    """
    if User.query.filter_by(email=e).first():
        return False
    return True


def validate_phone(p):
    """
    Verify if the phone number has not been used.
    :param p:   phone number
    """
    if User.query.filter_by(phone=p).first():
        return False
    return True


def validate_id(sw):
    """
    Verify if the student number or working number has not been used.
    :param sw:   stu_wor_id
    """
    if User.query.filter_by(stu_wor_id=sw).first():
        return False
    return True


def get_role_false():
    """
    for other modules to alter the global variable get_role_from_button
    """
    global get_role_from_button
    get_role_from_button = False


def get_role_true():
    """
    for other modules to alter the global variable get_role_from_button
    """
    global get_role_from_button
    get_role_from_button = True

