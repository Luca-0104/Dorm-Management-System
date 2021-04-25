from flask import request, redirect, render_template, url_for
from flask_login import login_required, current_user

from app.main import main
from app.auth.views import get_role_true

# The index page ----------------------------------------------------------------------------------------------
from app.models import User, Student, Guest


@main.route('/', methods=['GET', 'POST'])
def index():
    get_role_true()  # if we are in the index page, we should get ready for getting the role_id
    return render_template("samples/myindex.html")


# Three home pages for three kinds of users ----------------------------------------------------------------------------------------------
@main.route('/home_stu', methods=['GET', 'POST'])
def home_stu():
    return render_template("samples/studentHomepage.html")  # 待核对完善


@main.route('/home_dorm_admin', methods=['GET', 'POST'])
def home_dorm_admin():
    isSuccessful = request.args.get('isSuccessful', "True")
    pagenum = int(request.args.get('page', 1))
    pagination = Student.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template('samples/dormStudents.html', pagination=pagination, enterType='home', isSuccessful=isSuccessful, function='students')


@main.route('/home_dorm_admin_gue', methods=['GET', 'POST'])
def home_dorm_admin_gue():
    isSuccessful = request.args.get('isSuccessful', "True")
    pagenum = int(request.args.get('page', 1))
    pagination = Guest.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template('samples/dormGuests.html', pagination=pagination, enterType='home', isSuccessful=isSuccessful, function="guests")



@main.route('/home_sys_admin', methods=['GET', 'POST'])
def home_sys_admin():
    return render_template("samples/systemIndex.html",function="index")  # 待核对完善


@main.route('/home_sys_gue', methods=['GET', 'POST'])
def home_sys_gue():
    return render_template("samples/systemGuests.html",function="guests" )  # 待核对完善


@main.route('/home_sys_stu', methods=['GET', 'POST'])
def home_sys_stu():
    return render_template("samples/systemStudents.html",function="students")  # 待核对完善


@main.route('/home_sys_dorm', methods=['GET', 'POST'])
def home_sys_dorm():
    return render_template("samples/systemDorm.html",function="dormAdmin")  # 待核对完善




# The profile page ----------------------------------------------------------------------------------------------
@main.route('/user/<username>')
def user_profile(username):
    u = User.query.filter_by(user_name=username).first_or_404()
    if u.role_id == 1:
        stu = Student.query.filter_by(stu_number=u.stu_wor_id).first()
        return render_template('student.html', user=u, student=stu)  # 待核对完善
    elif u.role_id == 2:
        return render_template('dormAdmin.html', user=u)  # 待核对完善
    elif u.role_id == 3:
        return render_template('sysAdmin.html', user=u)  # 待核对完善


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_name = current_user.user_name
    stu_wor_id = current_user.stu_wor_id
    phone = current_user.phone
    email = current_user.email
    member_since = current_user.member_since

    if request.method == 'POST':
        # 待核对完善
        user_name = request.form.get('user_name')
        stu_wor_id = request.form.get('stu_wor_id')
        phone = request.form.get('phone')
        email = request.form.get('email')
        about_me = request.form.get('about_me')
        college = request.form.get('college')
        building_id = request.form.get('building_id')
        room_number = request.form.get('room_number')

        user = User.query.filter_by(stu_wor_id=stu_wor_id).first()
        according_stu = Student.query.filter_by(stu_number=stu_wor_id).first()

        # 待补全
        user.user_name = user_name

    return render_template('.html', user_name=user_name, stu_wor_id=stu_wor_id, phone=phone, email=email, member_since=member_since)  # 待核对完善
