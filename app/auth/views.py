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

## 注册
@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        stu_wor_id = request.form.get('stu_wor_id')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not all([username, studentid, password, password2]):
            flash('elements are incomplete')
        elif password != password2:
            flash('')
        else:
            new_user = Users(user_name=username, password=password, email=email, stu_wor_id=stu_wor_id)
            db.session.add(new_user)
            db.session.commit()
            return ''
    return render_template('register.html')


