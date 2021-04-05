from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from . import auth
from .. import db
from ..main import main
from ..models import User
from .forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_required, login_user, current_user


# Updates the last access time of the logged-in user
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:       # Determine whether the current user is logged in
        current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        stu_wor_id = request.form.get('stu_wor_id')     # 向前端索要学工号
        password = request.form.get('password')
        user = User.query.filter_by(stu_wor_id=stu_wor_id).first()
        if user is not None and user.verify_password(password):
            return "login successfully"            # 少路由，指向home界面
        else:
            flash('Invalid id or password.')
    return render_template('samples/login-2.html')


# Logout
@auth.route('/logout')
@login_required     # Make sure the user want to logout has logged in
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


# register
@auth.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        stu_wor_id = request.form.get('stu_wor_id')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not all([username, stu_wor_id, email, password, password2]):
            flash('elements are incomplete')
        elif password != password2:
            flash('Two passwords do not match')
        else:
            new_user = User(user_name=username, role_id=main.role_id,  password=password, email=email, stu_wor_id=stu_wor_id)
            flash('Registered successfully! You can login now.')
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))
    return render_template('samples/register-2.html')


