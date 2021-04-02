from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_required, login_user, current_user


# 更新已登录用户的最后访问时间
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:       # 判断当前用户是否已登录
        current_user.ping()


def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user_list = User.query.filter_by(username = username)
        for u in user_list:
            if u.password == new_password:
                return render_template('user/')
            else:
                return render_template('user/login.html',msg='用户名或者密码有误')