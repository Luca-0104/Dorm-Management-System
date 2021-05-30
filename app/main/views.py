import os
import time
from datetime import datetime, timedelta

from flask import request, redirect, render_template, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_
from werkzeug.utils import secure_filename

from app import db
from app.main import main
from app.auth.views import get_role_true

from app.models import User, Student, Guest, Repair, Complain, DormBuilding, DAdmin, Lost, Found
from app.student.views import ALLOWED_EXTENSIONS
from config import Config


@main.route('/', methods=['GET', 'POST'])
def index():
    """
    The initial index page for choosing a role to login or signup
    """
    get_role_true()  # if we are in the index page, we should get ready for getting the role_id
    return render_template("samples/myindex.html")


@main.route('/change_avatar', methods=['GET', 'POST'])
def change_avatar():
    """
    The function for users to change their avatars
    """
    if request.method == 'POST':
        icon = request.files.get('icon')  # able to be blank in the database, but we will not allow this happens
        icon_name = icon.filename
        suffix = icon_name.rsplit('.')[-1]

        if suffix in ALLOWED_EXTENSIONS:
            # save the photo into the dir: static/upload/avatar
            icon_name = secure_filename(icon_name)
            icon_name = icon_name[0:-4] + '__' + str(current_user.id) + '__' + icon_name[-4:]
            file_path = os.path.join(Config.avatar_dir, icon_name).replace('\\', '/')
            icon.save(file_path)

            # update the attribute in database that refers to the directory of the photo
            path = 'upload/avatar'
            pic = os.path.join(path, icon_name).replace('\\', '/')
            current_user.icon = pic
            db.session.commit()

            if current_user.role_id == 1:
                return redirect(url_for('main.home_stu'))
            elif current_user.role_id == 2:
                return redirect(url_for('main.home_dorm_admin_index'))
            elif current_user.role_id == 3:
                return redirect(url_for('main.home_sys_admin'))

        else:
            msg = 'The suffix of the picture should be jpg, gif, png and bmp only.'
            if current_user.role_id == 1:
                return redirect(url_for('main.home_stu', msg=msg))
            elif current_user.role_id == 2:
                return redirect(url_for('main.profile', msg=msg))
            elif current_user.role_id == 3:
                return redirect(url_for('main.profile', msg=msg))


# ----------------------------------------------- profiles for the users with different role  -----------------------------------------------


@main.route('/profile')
def profile():
    role_id = current_user.role_id
    stu_wor_id = current_user.stu_wor_id

    if role_id == 1:
        stu = Student.query.filter_by(stu_number=stu_wor_id).first()
        return render_template('samples/studentIndex.html', user=current_user, stu=stu)

    elif role_id == 2:
        da = DAdmin.query.filter_by(da_number=stu_wor_id).first()
        return render_template('samples/dormProfile.html', user=current_user, da=da)

    elif role_id == 3:
        return render_template('samples/systemProfile.html', user=current_user)


@main.route('/check_profile')
def check_profile():
    """
        When clicking on the avatar of a user, the profile of this user can be checked
    """
    role_id = request.args.get('role_id')
    uid = request.args.get('uid')
    user = User.quer.get(uid)
    stu_wor_id = user.stu_wor_id

    if role_id == 1:
        stu = Student.query.filter_by(stu_number=stu_wor_id).first()
        return render_template('samples/.html', user=user, stu=stu)     # 待核对

    elif role_id == 2:
        da = DAdmin.query.filter_by(da_number=stu_wor_id).first()
        return render_template('samples/.html', user=user, da=da)       # 待核对

    elif role_id == 3:
        return render_template('samples/.html', user=user)              # 待核对


@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """
        A method for editing the profile
    """
    role_id = current_user.role_id
    stu_wor_id = current_user.stu_wor_id

    if request.method == 'POST':

        phone = request.form.get('phone')
        email = request.form.get('email')

        # update the stu, da, sa tables
        if role_id == 1:
            stu = Student.query.filter_by(stu_number=stu_wor_id).first()
            if validate_stu_phone(phone):
                stu.phone = phone
            if validate_stu_email(email):
                stu.email = email
            db.session.add(stu)

        elif role_id == 2:
            da = DAdmin.query.filter_by(da_number=stu_wor_id).first()
            if validate_da_phone(phone):
                da.phone = phone
            if validate_da_email(email):
                da.email = email
            db.session.add(da)

        elif role_id == 3:
            pass

        # update the user table
        if validate_user_phone(phone):
            current_user.phone = phone
        if validate_user_email(email):
            current_user.email = email

        db.session.commit()




def validate_stu_phone(p):
    """
    Verify if the phone number has not been used in student table.
    :param p:   phone number
    """
    if len(p) == 11:
        print('phone ok')
        stu = Student.query.filter_by(phone=p).first()
        if stu:
            if not stu.is_deleted:
                return False
            return True
        return True
    return False


def validate_da_phone(p):
    """
    Verify if the phone number has not been used in dorm admin table.
    :param p:   phone number
    """
    if len(p) == 11:
        print('phone ok')
        da = DAdmin.query.filter_by(phone=p).first()
        if da:
            if not da.is_deleted:
                return False
            return True
        return True
    return False


def validate_user_phone(p):
    """
    Verify if the phone number has not been used in user table.
    :param p:   phone number
    """
    if len(p) == 11:
        print('phone ok')
        user = User.query.filter_by(phone=p).first()
        if user:
            if not user.is_deleted:
                return False
            return True
        return True
    return False


def validate_stu_email(e):
    """
    Verify if the email has not been used in student table.
    :param e:   email
    """
    if e.find('@', 1, len(e)) > 0:
        print('email ok')
        stu = Student.query.filter_by(email=e).first()
        if stu:
            if not stu.is_deleted:
                return False
            return True
        return True
    return False


def validate_da_email(e):
    """
    Verify if the email has not been used in dorm admin table.
    :param e:   email
    """
    if e.find('@', 1, len(e)) > 0:
        print('email ok')
        da = DAdmin.query.filter_by(email=e).first()
        if da:
            if not da.is_deleted:
                return False
            return True
        return True
    return False


def validate_user_email(e):
    """
    Verify if the email has not been used in user table.
    :param e:   email
    """
    if e.find('@', 1, len(e)) > 0:
        print('email ok')
        user = User.query.filter_by(email=e).first()
        if user:
            if not user.is_deleted:
                return False
            return True
        return True
    return False


# ----------------------------------------------- main pages of students  -----------------------------------------------


@main.route('/home_stu', methods=['GET', 'POST'])
def home_stu():
    """
    The index page for student users, which is the first page shown after login
    (Some basic information)
    """
    msg = request.args.get('msg')
    stu_number = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_number).first()

    return render_template("samples/studentIndex.html", function="index", stu=stu, msg=msg, user=current_user)  # 待核对完善


@main.route('/home_stu_bill', methods=['GET', 'POST'])
def home_stu_bill():
    return render_template("samples/studentBills.html", function="bills")  # 待核对


@main.route('/home_stu_complain', methods=['GET', 'POST'])
def home_stu_complain():
    pagenum = int(request.args.get('page', 1))
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    stu_id = stu.id
    pagination = Complain.query.filter_by(stu_id=stu_id).paginate(page=pagenum, per_page=5)
    return render_template("samples/studentComplain.html", pagination=pagination, enterType='home',
                           function="complain")  # 待核对


@main.route('/home_stu_repair', methods=['GET', 'POST'])
def home_stu_repair():
    pagenum = int(request.args.get('page', 1))
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    stu_id = stu.id
    pagination = Repair.query.filter_by(stu_id=stu_id).paginate(page=pagenum, per_page=5)
    return render_template("samples/studentRepair.html", pagination=pagination, enterType='home',
                           function="repair")  # 待核对


@main.route('/home_stu_lost_and_found', methods=['GET', 'POST'])
def home_stu_LAF():
    return render_template("samples/studentLF.html", function="lost and found")


@main.route('/home_stu_message', methods=['GET', 'POST'])
def home_stu_message():
    stu_number = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_number).first()

    repair_num = len(stu.repairs)
    complain_num = len(stu.complains)
    notification_num = 0

    building = stu.building
    da_list = building.dormAdmins
    for da in da_list:
        notification_num += len(da.notifications)

    # a dict stores the number of each kind of message
    mes_num_dict = {'repair': repair_num, 'complain': complain_num, 'notification': notification_num}

    return render_template("samples/studentMessage.html", function="message", mes_num_dict=mes_num_dict)


@main.route('/home_stu_lost', methods=['GET', 'POST'])
def home_stu_lost():
    """
    Shows only the lost information of this student himself (about me)
    """
    pagenum = int(request.args.get('page', 1))
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    stu_id = stu.id
    pagination = Lost.query.filter_by(stu_id=stu_id, is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template("samples/aboutMe.html", pagination=pagination, enterType='home',
                           function="lost and found", lnf_type='lost')  # 待核对


@main.route('/home_stu_found', methods=['GET', 'POST'])
def home_stu_found():
    """
    Shows only the found information of this student himself (about me)
    """
    pagenum = int(request.args.get('page', 1))
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    stu_id = stu.id
    pagination = Found.query.filter_by(stu_id=stu_id, is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template("samples/aboutMe.html", pagination=pagination, enterType='home',
                           function="lost and found", lnf_type='found')  # 待核对


@main.route('/home_stu_lost_and_found', methods=['GET', 'POST'])
def home_stu_lost_and_found():
    stu_number = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_number).first()

    return render_template("samples/studentLF.html", function="lost and found")  # 待核对


# ----------------------------------------------- main pages of dormitory administrator -----------------------------------------------


@main.route('/home_dorm_admin', methods=['GET', 'POST'])
def home_dorm_admin():
    isSuccessful = request.args.get('isSuccessful', "True")
    pagenum = int(request.args.get('page', 1))
    pagination = Student.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template('samples/dormStudents.html', pagination=pagination, enterType='home',
                           isSuccessful=isSuccessful, function='students')


@main.route('/home_dorm_admin_gue', methods=['GET', 'POST'])
def home_dorm_admin_gue():
    isSuccessful = request.args.get('isSuccessful', "True")
    pagenum = int(request.args.get('page', 1))
    pagination = Guest.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template('samples/dormGuests.html', pagination=pagination, enterType='home',
                           isSuccessful=isSuccessful, function="guests")


@main.route('/home_da_lost_and_found', methods=['GET', 'POST'])
def home_da_lost_and_found():
    return render_template('samples/dormLF.html', function="lost and found")  # 待核对


@main.route('/home_dorm_admin_message', methods=['GET', 'POST'])
def home_dorm_admin_message():
    da_number = current_user.stu_wor_id
    da = DAdmin.query.filter_by(da_number=da_number).first()

    repair_num = 0
    complain_num = 0
    notification_num = 0

    building = da.building
    stu_list = building.students
    da_list = building.dormAdmins
    for stu in stu_list:
        repair_num += len(stu.repairs)
        complain_num += len(stu.complains)
    for da in da_list:
        notification_num += len(da.notifications)

    # a dict stores the number of each kind of message
    mes_num_dict = {'repair': repair_num, 'complain': complain_num, 'notification': notification_num}

    return render_template('samples/dormMessage.html', function="message", mes_num_dict=mes_num_dict)


@main.route('/home_dorm_admin_index', methods=['GET', 'POST'])
def home_dorm_admin_index():
    """
    A function for showing the data graphs in the initial page of dorm administrator
    Only the data about the building that this dorm administrator takes charge of
    (The index function of dorm administrators)
    """
    msg = request.args.get('msg')
    work_num = current_user.stu_wor_id
    da = DAdmin.query.filter_by(da_number=work_num).first()
    building = da.building

    da_list = building.dormAdmins
    stu_list = building.students
    gue_list = []
    for stu in stu_list:
        gues = stu.guests
        for gue in gues:
            if gue not in gue_list:
                gue_list.append(gue)

    # ******************** for graph 1 ********************
    repair_list = []
    complain_list = []
    notification_list = []

    for stu in stu_list:
        repairs = stu.repairs
        for repair in repairs:
            if repair not in repair_list:
                repair_list.append(repair)

    for stu in stu_list:
        complains = stu.complains
        for complain in complains:
            if complain not in complain_list:
                complain_list.append(complain)

    for da in da_list:
        notifications = da.notifications
        for n in notifications:
            if n not in notification_list:
                notification_list.append(n)

    mes_num = len(repair_list) + len(complain_list) + len(notification_list)

    # a dict stores the number of students, guests and messages of this building
    basic_number_dict = {'stu_num': len(stu_list), 'gue_num': len(gue_list), 'mes_num': mes_num}

    # ******************** for graph 2 ********************
    floor1 = 0
    floor2 = 0
    floor3 = 0
    floor4 = 0
    floor5 = 0
    floor6 = 0
    for stu in stu_list:
        floor = stu.room_number // 100
        if floor == 1:
            floor1 += 1
        elif floor == 2:
            floor2 += 1
        elif floor == 3:
            floor3 += 1
        elif floor == 4:
            floor4 += 1
        elif floor == 5:
            floor5 += 1
        elif floor == 6:
            floor6 += 1

    # a list of number of students in each floor
    floor_stu_num_list = [floor1, floor2, floor3, floor4, floor5, floor6]

    # ******************** for graph 3 ********************
    bdic = 0
    fhss = 0
    fit = 0
    fmm = 0
    fuc = 0
    fs = 0
    fels = 0
    cem = 0
    cad = 0
    fhc = 0

    for stu in stu_list:
        if stu.college == 'Beijing Dublin International College':
            bdic += 1
        elif stu.college == 'Faculty of Humanities and Social Sciences':
            fhss += 1
        elif stu.college == 'Faculty of Information Technology':
            fit += 1
        elif stu.college == 'Faculty of Materials and Manufacturing':
            fmm += 1
        elif stu.college == 'Faculty of Urban Construction':
            fuc += 1
        elif stu.college == 'Faculty of Science':
            fs += 1
        elif stu.college == 'Faculty of Environment and Life Sciences':
            fels += 1
        elif stu.college == 'College of Economic and Management':
            cem += 1
        elif stu.college == 'College of Art and Design':
            cad += 1
        elif stu.college == 'FanGongXiu Honors College':
            fhc += 1

    # a dict for storing the number of students of each college in this building
    college_dict = {'BDIC': bdic, 'FHSS': fhss, 'FIT': fit, 'FMM': fmm, 'FUC': fuc, 'FS': fs, 'FELS': fels,
                    'CEM': cem, 'CAD': cad, 'FHC': fhc}

    # ******************** for graph 4 ********************
    year_now = time.localtime().tm_year % 1000 % 100  # for today, year_now should be 21
    month_now = time.localtime().tm_mon  # for today, month_now should be 5

    stage1 = 0
    stage2 = 0
    stage3 = 0
    stage4 = 0

    for stu in stu_list:
        stu_number = stu.stu_number
        year = int(stu_number[0:2])

        if 9 <= month_now <= 12:  # the first semester of the year
            diff = year_now - year
            if diff == 0:
                stage1 += 1
            elif diff == 1:
                stage2 += 1
            elif diff == 2:
                stage3 += 1
            elif diff == 3:
                stage4 += 1

        else:  # the second semester of the year
            diff = year_now - year
            if diff == 1:
                stage1 += 1
            elif diff == 2:
                stage2 += 1
            elif diff == 3:
                stage3 += 1
            elif diff == 4:
                stage4 += 1

    # a list stores the numbers of students in different stage, ordered from stage1 to stage4
    stage_list = [stage1, stage2, stage3, stage4]

    # ******************** for graph 5 ********************
    gue1 = 0
    gue2 = 0
    gue3 = 0
    gue4 = 0
    gue5 = 0
    gue6 = 0
    gue7 = 0

    for gue in gue_list:
        if (datetime.utcnow() - gue.arrive_time).days == 0:
            gue1 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 1:
            gue2 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 2:
            gue3 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 3:
            gue4 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 4:
            gue5 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 5:
            gue6 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 6:
            gue7 += 1

    d1 = datetime.now()
    d2 = d1 + timedelta(days=-1)
    d3 = d2 + timedelta(days=-1)
    d4 = d3 + timedelta(days=-1)
    d5 = d4 + timedelta(days=-1)
    d6 = d5 + timedelta(days=-1)
    d7 = d6 + timedelta(days=-1)

    day1 = d1.strftime('%Y-%m-%d')
    day2 = d2.strftime('%Y-%m-%d')
    day3 = d3.strftime('%Y-%m-%d')
    day4 = d4.strftime('%Y-%m-%d')
    day5 = d5.strftime('%Y-%m-%d')
    day6 = d6.strftime('%Y-%m-%d')
    day7 = d7.strftime('%Y-%m-%d')

    # a 2D list stores the date (str) and numbers of guests (int) in this building in last 7 days, they are ordered from today to 7 days ago
    gue_num_list = [[day1, gue1], [day2, gue2], [day3, gue3], [day4, gue4], [day5, gue5], [day6, gue6], [day7, gue7]]

    return render_template('samples/dormIndex.html', function="index", msg=msg,
                           basic_number_dict=basic_number_dict,  # graph1
                           floor_stu_num_list=floor_stu_num_list,  # graph2
                           college_dict=college_dict,  # graph3
                           stage_list=stage_list,  # graph4
                           gue_num_list=gue_num_list  # graph5
                           )


# ----------------------------------------------- main pages of system administrator -----------------------------------------------

@main.route('/home_sys_admin', methods=['GET', 'POST'])
def home_sys_admin():
    """
    A function for showing the data graphs in the initial page of system administrator
    (The index function of system administrators)
    """
    msg = request.args.get('msg')

    building_id = request.args.get('building_id', '0')

    # building_id == 0 means this is the initial login status (before selecting a specific dorm building),
    # which will show the information of all the dorm buildings
    if building_id == '0':
        stu_list = Student.query.all()
        da_list = DAdmin.query.all()
        gue_list = Guest.query.all()
    else:
        building = DormBuilding.query.filter_by(id=building_id).first()
        stu_list = building.students
        da_list = building.dormAdmins
        gue_list = []
        for stu in stu_list:
            gues = stu.guests
            for gue in gues:
                if gue not in gue_list:
                    gue_list.append(gue)

    # ******************** for graph 1 ********************
    # a dict stores the number of students, dorm administrators and guests
    basic_number_dict = {'stu_num': len(stu_list), 'da_num': len(da_list), 'gue_num': len(gue_list)}

    # ******************** for graph 2 ********************
    floor1 = 0
    floor2 = 0
    floor3 = 0
    floor4 = 0
    floor5 = 0
    floor6 = 0
    for stu in stu_list:
        floor = stu.room_number // 100
        if floor == 1:
            floor1 += 1
        elif floor == 2:
            floor2 += 1
        elif floor == 3:
            floor3 += 1
        elif floor == 4:
            floor4 += 1
        elif floor == 5:
            floor5 += 1
        elif floor == 6:
            floor6 += 1

    # a list of number of students in each floor
    floor_stu_num_list = [floor1, floor2, floor3, floor4, floor5, floor6]

    # ******************** for graph 3 ********************
    bdic = 0
    fhss = 0
    fit = 0
    fmm = 0
    fuc = 0
    fs = 0
    fels = 0
    cem = 0
    cad = 0
    fhc = 0

    for stu in stu_list:
        if stu.college == 'Beijing Dublin International College':
            bdic += 1
        elif stu.college == 'Faculty of Humanities and Social Sciences':
            fhss += 1
        elif stu.college == 'Faculty of Information Technology':
            fit += 1
        elif stu.college == 'Faculty of Materials and Manufacturing':
            fmm += 1
        elif stu.college == 'Faculty of Urban Construction':
            fuc += 1
        elif stu.college == 'Faculty of Science':
            fs += 1
        elif stu.college == 'Faculty of Environment and Life Sciences':
            fels += 1
        elif stu.college == 'College of Economic and Management':
            cem += 1
        elif stu.college == 'College of Art and Design':
            cad += 1
        elif stu.college == 'FanGongXiu Honors College':
            fhc += 1

    # a dict for storing the number of students of each college in this building
    college_dict = {'BDIC': bdic, 'FHSS': fhss, 'FIT': fit, 'FMM': fmm, 'FUC': fuc, 'FS': fs, 'FELS': fels, 'CEM': cem, 'CAD': cad, 'FHC': fhc}

    # ******************** for graph 4 ********************
    year_now = time.localtime().tm_year % 1000 % 100    # for today, year_now should be 21
    month_now = time.localtime().tm_mon                 # for today, month_now should be 5

    stage1 = 0
    stage2 = 0
    stage3 = 0
    stage4 = 0

    for stu in stu_list:
        stu_number = stu.stu_number
        year = int(stu_number[0:2])

        if 9 <= month_now <= 12:  # the first semester of the year
            diff = year_now - year
            if diff == 0:
                stage1 += 1
            elif diff == 1:
                stage2 += 1
            elif diff == 2:
                stage3 += 1
            elif diff == 3:
                stage4 += 1

        else:                       # the second semester of the year
            diff = year_now - year
            if diff == 1:
                stage1 += 1
            elif diff == 2:
                stage2 += 1
            elif diff == 3:
                stage3 += 1
            elif diff == 4:
                stage4 += 1

    # a list stores the numbers of students in different stage, ordered from stage1 to stage4
    stage_list = [stage1, stage2, stage3, stage4]

    # ******************** for graph 5 ********************
    gue1 = 0
    gue2 = 0
    gue3 = 0
    gue4 = 0
    gue5 = 0
    gue6 = 0
    gue7 = 0

    for gue in gue_list:
        if (datetime.utcnow() - gue.arrive_time).days == 0:
            gue1 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 1:
            gue2 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 2:
            gue3 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 3:
            gue4 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 4:
            gue5 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 5:
            gue6 += 1
        elif (datetime.utcnow() - gue.arrive_time).days == 6:
            gue7 += 1

    d1 = datetime.now()
    d2 = d1 + timedelta(days=-1)
    d3 = d2 + timedelta(days=-1)
    d4 = d3 + timedelta(days=-1)
    d5 = d4 + timedelta(days=-1)
    d6 = d5 + timedelta(days=-1)
    d7 = d6 + timedelta(days=-1)

    day1 = d1.strftime('%Y-%m-%d')
    day2 = d2.strftime('%Y-%m-%d')
    day3 = d3.strftime('%Y-%m-%d')
    day4 = d4.strftime('%Y-%m-%d')
    day5 = d5.strftime('%Y-%m-%d')
    day6 = d6.strftime('%Y-%m-%d')
    day7 = d7.strftime('%Y-%m-%d')

    # a 2D list stores the date (str) and numbers of guests (int) in this building in last 7 days, they are ordered from today to 7 days ago
    gue_num_list = [[day1, gue1], [day2, gue2], [day3, gue3], [day4, gue4], [day5, gue5], [day6, gue6], [day7, gue7]]

    return render_template("samples/systemIndex.html", function="index", building_id=building_id, msg=msg,
                           basic_number_dict=basic_number_dict,  # graph1
                           floor_stu_num_list=floor_stu_num_list,  # graph2
                           college_dict=college_dict,  # graph3
                           stage_list=stage_list,  # graph4
                           gue_num_list=gue_num_list  # graph5
                           )  # 待核对完善


@main.route('/home_sys_gue', methods=['GET', 'POST'])
def home_sys_gue():
    building_id = request.args.get('building_id', '0')
    pagenum = int(request.args.get('page', 1))
    if building_id == '0':
        pagination = Guest.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    else:
        pagination = Guest.query.join(Student).filter(and_(Student.building_id == building_id, Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)

    return render_template("samples/systemGuests.html", function="guests", building_id=building_id, enterType='home', pagination=pagination)


@main.route('/home_sys_stu', methods=['GET', 'POST'])
def home_sys_stu():
    building_id = request.args.get('building_id', '0')
    isSuccessful = request.args.get('isSuccessful', "True")
    pagenum = int(request.args.get('page', 1))

    if building_id == '0':
        pagination = Student.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    else:
        pagination = Student.query.filter_by(is_deleted=False, building_id=building_id).paginate(page=pagenum, per_page=5)

    return render_template('samples/systemStudents.html', pagination=pagination, enterType='home', isSuccessful=isSuccessful, function='students', building_id=building_id)


@main.route('/home_sys_dorm', methods=['GET', 'POST'])
def home_sys_dorm():
    pagenum = int(request.args.get('page', 1))
    pagination = DAdmin.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template("samples/systemDorm.html", function="dormAdmin", pagination=pagination, enterType='home')  # 待核对完善


@main.route('/home_sys_lost_and_found')
def home_sys_lost_and_found():
    return render_template('samples/sysLF.html', function="lost and found")  # 待核对
