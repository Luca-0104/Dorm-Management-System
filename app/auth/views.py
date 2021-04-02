from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_required, login_user, current_user


# Updates the last access time of the logged-in user
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:       # Determine whether the current user has logged in
        current_user.ping()


@auth.route('login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        stu_wor_id = request.form.get('stu_wor_id')     # 向前端索要学工号
        password = request.form.get('password')
        user = User.query.filter_by(stu_wor_id=stu_wor_id).first()
        if user is not None and user.verify_password(password):
            return redirect(url_for('main.'))              # 少路由，指向home界面
        else:
            flash('Invalid id or password.')
    return render_template('user/login.html')


# Logout
@auth.route('/logout')
@login_required     # Make sure the user want to logout has logged in
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
