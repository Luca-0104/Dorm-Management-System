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


@auth.route('login/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username') #改成学工号
        password = request.form.get('password')
        user = User.query.filter_by(user_name=username).first()
        if user is not None and user.verify_password(password):
            return redirect(url_for()) #少路由
        else:
            flash('学工号或密码错误') #改成英文
    return render_template('user/login.html')
