from flask import request, redirect, render_template, url_for

from app.main import main
from app.auth.views import get_role_true


@main.route('/', methods=['GET', 'POST'])
def index():
    get_role_true()  # if we are in the index page, we should get ready for getting the role_id
    return render_template("samples/myindex.html")


@main.route('/home_stu', methods=['GET', 'POST'])
def home_stu():
    return render_template(".html")  # 待核对完善


@main.route('/home_dorm_admin', methods=['GET', 'POST'])
def home_dorm_admin():
    return render_template(".html")  # 待核对完善


@main.route('/home_sys_admin', methods=['GET', 'POST'])
def home_sys_admin():
    return render_template(".html")  # 待核对完善
