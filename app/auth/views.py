from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, jsonify
from wtforms import ValidationError

from . import auth
from .. import db
from ..main import main
from ..models import User, Student
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
    isSuccessful = True

    if request.method == 'POST':
        get_role_from_button = False
        stu_wor_id = request.form.get('stu_wor_id')
        password = request.form.get('password')
        user = User.query.filter_by(stu_wor_id=stu_wor_id).first()
        if user is not None:

            print(role_id)
            print(user.role_id)
            # Only when trying to login with the corresponding role can be allowed
            # Otherwise, you will be sent back to the index page
            # role_id means the role has been chosen in the index page
            # while user.role_id means the role of the user who is trying to login
            if role_id == user.role_id:
                if user is not None and user.verify_password(password):
                    login_user(user)
                    isSuccessful = True
                    if role_id == 1:
                        url = 'main.home_stu'
                    elif role_id == 2:
                        url = 'main.home_dorm_admin_index'
                    elif role_id == 3:
                        url = 'main.home_sys_admin'
                    return redirect(url_for(url))
                else:
                    # flash('Invalid id or password.')
                    isSuccessful = False
            else:
                return redirect(url_for('main.index'))

        else:
            isSuccessful = False

    # decide if we need to get the role_id again
    if request.method == 'GET' and get_role_from_button is True:
        role_id = int(request.args.get('identification'))
        print(role_id)

    getf = request.args.get('f')
    if getf is not None:
        getf = int(getf)
    if getf == 1:
        return render_template('samples/phoneLogin.html', role_id=role_id, isSuccessful=isSuccessful)
    if getf == 2:
        return render_template('samples/emailLogin.html', role_id=role_id, isSuccessful=isSuccessful)
    return render_template('samples/login-2.html', role_id=role_id, isSuccessful=isSuccessful)


# Logout
@auth.route('/logout')
@login_required  # Make sure the user want to logout has logged in
def logout():
    logout_user()
    # flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/sendMsg')
def send_message():
    pass


@auth.route('/home')
def home():
    pagenum = int(request.args.get('page', 1))
    pagination = Student.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template('samples/testindex.html', pagination=pagination)


# register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    global get_role_from_button
    isSuccessful = True

    if request.method == 'POST':
        username = request.form.get('username')
        stu_wor_id = request.form.get('stu_wor_id')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not all([username, stu_wor_id, email, phone, password, password2]):
            # flash('elements are incomplete')
            print('elements are incomplete')
            isSuccessful = False

        elif password != password2:
            # flash('Two passwords do not match')
            print('Two passwords do not match')
            isSuccessful = False

        else:
            print(validate_email(email))
            print(validate_phone(phone))
            print(validate_id(stu_wor_id))

            if validate_email(email) and validate_phone(phone) and validate_id(stu_wor_id):
                new_user = User(user_name=username, stu_wor_id=stu_wor_id, role_id=role_id, password=password,
                                email=email, phone=phone)

                # flash('Registered successfully! You can login now.')
                isSuccessful = True
                db.session.add(new_user)
                db.session.commit()

                # Change the according student status to is_registered
                stu = Student.query.filter_by(stu_number=stu_wor_id).first()
                if stu is not None:
                    stu.register_stu()

                get_role_from_button = False  # we will go back to the login page and in this case we do not need to get the role_id again
                return redirect(url_for("auth.login"))

    return render_template('samples/register-2.html', role_id=role_id, isSuccessful=isSuccessful)


@auth.route('checkID', methods=['GET', 'POST'])
def check_id():
    id = request.args.get('id')
    user = User.query.filter(User.stu_wor_id == id).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The ID has already existed")
    else:
        return jsonify(code=200, msg="this id number is available")


@auth.route('checkEmail', methods=['GET', 'POST'])
def check_email():
    email = request.args.get('email')
    user = User.query.filter(User.email == email).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The email has already existed")
    else:
        return jsonify(code=200, msg="this phone number is available")


@auth.route('checkPhone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The phone number has already existed")
    else:
        return jsonify(code=200, msg="this phone number is available")


@auth.route('checkPassword', methods=['GET', 'POST'])
def check_password():
    password = request.args.get('password')
    cpassword = request.args.get('cpassword')
    if password != cpassword:
        return jsonify(code=400, msg="The password is not match")
    else:
        return jsonify(code=200, msg="this phone number is available")


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
