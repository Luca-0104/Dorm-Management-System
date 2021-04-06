from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, jsonify
from wtforms import ValidationError

from app.auth.smsend import SmsSendAPIDemo
from . import auth
from .. import db
from ..main import main
from ..models import User
from flask_login import logout_user, login_required, login_user, current_user


# # Updates the last access time of the logged-in user
# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated:       # Determine whether the current user is logged in
#         current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            stu_wor_id = request.form.get('stu_wor_id')     # 向前端索要学工号
            password = request.form.get('password')
            user = User.query.filter_by(stu_wor_id=stu_wor_id).first()
            # return redirect(url_for('auth.home'))
            if user is not None and user.verify_password(password):
                redirect(url_for('auth.home'))           # 少路由，指向home界面
            else:
                flash('Invalid id or password.')
    # elif f==2:#手机验证登录

    global role_id
    role_id = int(request.args.get('identification'))
    print(role_id)
    getf = request.args.get('f')
    if getf != None:
        getf = int(getf)
    if getf == 1:
        return render_template('samples/phoneLogin.html',role_id=role_id)
    if getf == 2:
        return render_template('samples/emailLogin.html' ,role_id = role_id)
    return render_template('samples/login-2.html',role_id=role_id)


# Logout
@auth.route('/logout')
@login_required     # Make sure the user want to logout has logged in
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/sendMsg')
def send_message():
    phone = request.args.get('phone')
    SECRET_ID = "274e7c35c2db7a0e8ac5448dbf98a62b"  # 产品密钥ID，产品标识
    SECRET_KEY = "95fa465892538ed30133f262ca0bd4b6"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "71d6d283d3834c2eac2b3d0bde34e430"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID,SECRET_KEY,BUSINESS_ID)
    params = {
        "mobile": phone,
        "templateId": "10084",
        "paramType": "json",
        "params": "json格式字符串"
    }
    ret = api.send(params)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["data"]["taskId"]
            print("taskId = %s" % taskId)
        else:
            print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))

@auth.route('checkphone',methods=['GET','POST'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    if len(user)>0:
        return jsonify(code=400,msg="此号码已注册")
    else:
        return jsonify(code=200,msg="此号码可用")

@auth.route('/home')
def home():
    return  render_template('samples/homepage.html')


# register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("yes1")
        username = request.form.get('username')
        stu_wor_id = request.form.get('stu_wor_id')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not all([username, stu_wor_id, email, password, password2]):
            flash('elements are incomplete')
            print('elements are incomplete')

        elif password != password2:
            flash('Two passwords do not match')
            print('Two passwords do not match')

        else:
            print("yes2.1")
            print(validate_email(email))
            print(validate_phone(phone))
            print(validate_id(stu_wor_id))

            if validate_email(email) and validate_phone(phone) and validate_id(stu_wor_id):
                print("yes2.1.1")
                # new_user = User(user_name=username, role_id=main.role_id,  password=password, email=email, stu_wor_id=stu_wor_id, phone=phone)
                new_user = User(user_name=username,  password=password, email=email, stu_wor_id=stu_wor_id, phone=phone)
                flash('Registered successfully! You can login now.')
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("auth.login"))
            else:
                print("yes2.1.2")
                flash('Email, phone number or id already exists.')
    role_id = request.args.get('identification')
    return render_template('samples/register-2.html',role_id=role_id)


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


