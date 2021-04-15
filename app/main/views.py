from flask import request, redirect, render_template, url_for
from flask_login import login_required

from app.main import main
from app.auth.views import get_role_true

# The index page ----------------------------------------------------------------------------------------------
from app.models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    get_role_true()  # if we are in the index page, we should get ready for getting the role_id
    return render_template("samples/myindex.html")


# Three home pages for three kinds of users ----------------------------------------------------------------------------------------------
@main.route('/home_stu', methods=['GET', 'POST'])
def home_stu():
    return render_template(".html")  # 待核对完善


@main.route('/home_dorm_admin', methods=['GET', 'POST'])
def home_dorm_admin():
    return render_template(".html")  # 待核对完善


@main.route('/home_sys_admin', methods=['GET', 'POST'])
def home_sys_admin():
    return render_template(".html")  # 待核对完善


# The profile page ----------------------------------------------------------------------------------------------
@main.route('/user/<username>')
def user(username):
    u = User.query.filter_by(user_name=username).first_or_404()
    if u.role_id == 1:
        return render_template('student.html', user=u)  # 待核对完善
    elif u.role_id == 2:
        return render_template('dormAdmin.html', user=u)  # 待核对完善
    elif u.role_id == 3:
        return render_template('sysAdmin.html', user=u)  # 待核对完善


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    pass

