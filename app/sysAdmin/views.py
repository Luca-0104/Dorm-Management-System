from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import logout_user, login_required, login_user, current_user
from sqlalchemy import or_, and_, desc
from wtforms import ValidationError
from . import sysAdmin
from .. import db
from ..models import Student, Guest, DAdmin, Lost, Found


@sysAdmin.route('/search_stu', methods=['GET', 'POST'])
def search_stu():
    """
    fuzzy querying was used
    get a stu_list that is a list of Student objects that meet the filter requirement
    """
    building_id = request.args.get('building_id', '0')

    key_word = request.args.get('content')
    tag = request.args.get('tag')
    pagenum = int(request.args.get('page', 1))
    enter_type = 'search'
    is_successful = request.args.get('isSuccessful', "True")  # The default value is True

    if building_id == '0':
        if tag == 'all':
            stu_list = Student.query.filter(and_(or_(Student.stu_name.contains(key_word),
                                                     Student.stu_number.contains(key_word),
                                                     Student.phone.contains(key_word),
                                                     Student.college.contains(key_word),
                                                     Student.room_number.contains(key_word),
                                                     # Student.enroll_date.contains(key_word)
                                                     ), Student.is_deleted == False)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'stu_name':
            stu_list = Student.query.filter(
                and_(Student.stu_name.contains(key_word), Student.is_deleted == False)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'stu_number':
            stu_list = Student.query.filter(
                and_(Student.stu_number.contains(key_word), Student.is_deleted == False)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'phone':
            stu_list = Student.query.filter(
                and_(Student.phone.contains(key_word), Student.is_deleted == False)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'college':
            stu_list = Student.query.filter(
                and_(Student.college.contains(key_word), Student.is_deleted == False)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'room_number':
            stu_list = Student.query.filter(
                and_(Student.room_number.contains(key_word), Student.is_deleted == False)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        # elif tag == 'enroll_date':
        #     stu_list = Student.query.filter(and_(Student.enroll_date.contains(key_word), Student.is_deleted == False)).order_by(Student.room_number).paginate(page=pagenum, per_page=5)

    else:
        if tag == 'all':
            stu_list = Student.query.filter(
                and_(Student.building_id == building_id, or_(Student.stu_name.contains(key_word),
                                                             Student.stu_number.contains(key_word),
                                                             Student.phone.contains(key_word),
                                                             Student.college.contains(key_word),
                                                             Student.room_number.contains(key_word),
                                                             # Student.enroll_date.contains(key_word)
                                                             ), Student.is_deleted == False)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'stu_name':
            stu_list = Student.query.filter(
                and_(Student.stu_name.contains(key_word), Student.is_deleted == False,
                     Student.building_id == building_id)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'stu_number':
            stu_list = Student.query.filter(
                and_(Student.stu_number.contains(key_word), Student.is_deleted == False,
                     Student.building_id == building_id)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'phone':
            stu_list = Student.query.filter(
                and_(Student.phone.contains(key_word), Student.is_deleted == False,
                     Student.building_id == building_id)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'college':
            stu_list = Student.query.filter(
                and_(Student.college.contains(key_word), Student.is_deleted == False,
                     Student.building_id == building_id)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

        elif tag == 'room_number':
            stu_list = Student.query.filter(
                and_(Student.room_number.contains(key_word), Student.is_deleted == False,
                     Student.building_id == building_id)).order_by(
                Student.room_number).paginate(page=pagenum, per_page=5)

    return render_template('samples/testindex.html', pagination=stu_list, enterType=enter_type, content=key_word,
                           tag=tag, isSuccessful=is_successful, function='students')


# @sysAdmin.route('/delete_stu', endpoint='delete')
# def delete_stu():
#     id = request.args.get('id')
#     content = request.args.get('content')
#     tag = request.args.get('tag')
#     enter_type = request.args.get('enterType')
#     page = request.args.get('page')
#
#     student = Student.query.get(id)
#     student.is_deleted = True
#     db.session.add(student)
#     db.session.commit()
#
#     if enter_type == "home":
#         return redirect(url_for('main.home_sys_stu', page=page))
#     elif enter_type == "search":
#         return redirect(url_for('sysAdmin.search_stu', content=content, tag=tag, page=page))
#
#     return redirect(url_for('main.home_sys_stu', page=page))

#
# @sysAdmin.route('/add_stu', methods=['GET', 'POST'])
# def add_stu():
#     if request.method == 'POST':
#         stu_name = request.form.get('name')
#         stu_number = request.form.get('stu_ID')
#         phone = request.form.get('phone')
#         email = request.form.get('email')
#         college = request.form.get('college')
#         # building_id_str = request.form.get('building_id')
#         room_number_str = request.form.get('room')
#         # building_id = None
#         building_id = 1  # 暂时默认都给1，sprint3会将其改为宿管对应的楼号
#         room_number = None
#
#         # if building_id_str != '':
#         #     building_id = int(building_id_str)
#
#         if room_number_str != '':
#             room_number = int(room_number_str)
#
#         if stu_name != '' and stu_number != '' and phone != '' and email != '' and college != '' and building_id is not None and room_number is not None:
#             if validate_stu_number(stu_number) and validate_phone(phone) and validate_email(email):
#                 new_student = Student(stu_name=stu_name,
#                                       stu_number=stu_number,
#                                       phone=phone,
#                                       email=email,
#                                       college=college,
#                                       building_id=building_id,
#                                       room_number=room_number)
#                 db.session.add(new_student)
#                 db.session.commit()
#                 return redirect(url_for('main.home_sys_admin', isSuccessful=True))
#             else:
#                 return redirect(url_for('main.home_sys_admin', isSuccessful=False))
#         else:
#             return redirect(url_for('main.home_sys_admin', isSuccessful=False))
#
#     return render_template('samples/testindex.html', function='students')


# @sysAdmin.route('/update_stu', endpoint='update', methods=['GET', 'POST'])
# def update_stu():
#     building_id = request.args.get('building_id', '0')
#     id = request.args.get('id')
#     student = Student.query.get(id)
#     content = request.args.get('content')
#     tag = request.args.get('tag')
#     enter_type = request.args.get('enterType')
#     page = request.args.get('page')
#     is_changed = False
#     is_stop = False      # 判断是否要停止当前修改，防止一部分信息被改，一部分没改
#
#     if request.method == 'POST':
#         stu_name = request.form.get('name')
#         stu_number = request.form.get('stu_ID')
#         print("stu_number length: " + str(len(stu_number)))
#         phone = request.form.get('phone')
#         email = request.form.get('email')
#         college = request.form.get('college')
#         room_number_str = request.form.get('room')
#         room_number = None
#
#         if room_number_str != '':
#             room_number = int(room_number_str)
#
#         if stu_name != '':
#             student.stu_name = stu_name
#             is_changed = True
#
#         if stu_number != '':
#             if validate_stu_number(stu_number):
#                 student.stu_number = stu_number
#                 is_changed = True
#             else:
#                 is_stop = True
#
#         if phone != '':
#             if validate_phone(phone):
#                 student.phone = phone
#                 is_changed = True
#             else:
#                 is_stop = True
#
#         if email != '':
#             if validate_email(email):
#                 student.email = email
#                 is_changed = True
#             else:
#                 is_stop = True
#
#         if college != '':
#             student.college = college
#             is_changed = True
#
#         if room_number is not None:
#             student.room_number = room_number
#             is_changed = True
#
#         # 检查信息是否修改成功
#         if is_changed and not is_stop:
#             db.session.add(student)
#             db.session.commit()
#
#             if enter_type == "home":
#                 return redirect(url_for('main.home_sys_stu', page=page, isSuccessful="True", building_id=building_id))
#             elif enter_type == "search":
#                 return redirect(url_for('sysAdmin.search_stu', content=content, tag=tag, page=page, isSuccessful="True", building_id=building_id))
#         else:
#             if enter_type == "home":
#                 return redirect(url_for('main.home_sys_stu', page=page, isSuccessful="False", building_id=building_id))
#             elif enter_type == "search":
#                 return redirect(url_for('sysAdmin.search_stu', content=content, tag=tag, page=page, isSuccessful="False", building_id=building_id))
#
#     return render_template('samples/systemStudents.html', function='students', building_id=building_id)


def validate_stu_number(n):
    """
    Verify if the student number has not been used.
    :param n:   student number
    """
    if len(n) == 8:
        print('stu_number ok')
        stu = Student.query.filter_by(stu_number=n).first()
        if stu:
            if not stu.is_deleted:
                return False
            return True
        return True
    return False


def validate_phone(p):
    """
    Verify if the phone number has not been used.
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


def validate_email(e):
    """
    Verify if the email has not been used.
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


@sysAdmin.route('/dormAdd', methods=['GET', 'POST'])
def check_add():
    stu_number = request.args.get('id')
    id = Student.query.filter(Student.stu_number == stu_number).all()
    email = request.args.get('email')
    emails = Student.query.filter(Student.email == email).all()
    phone = request.args.get('phone')
    phones = Student.query.filter(Student.phone == phone).all()
    print(id, phone, email)
    if stu_number == "" or email == "" or phone == "":
        return jsonify(code=400, msg="You have to fill all the Information")
    if len(id) > 0 or len(emails) > 0 or len(phones) > 0:
        return jsonify(code=400, msg="Some Information is invalid")
    if not validate_email(email) or not validate_phone(phone) or not validate_stu_number(stu_number):
        return jsonify(code=400, msg="Some Information is invalid")
    else:
        return jsonify(code=200, msg="This Phone number is available")


@sysAdmin.route('/dormModify', methods=['GET', 'POST'])
def check_modify():
    print("yes")
    stu_id = request.args.get('id')
    id = Student.query.filter(Student.stu_number == stu_id).all()
    email = request.args.get('email')
    emails = Student.query.filter(Student.email == email).all()
    phone = request.args.get('phone')
    phones = Student.query.filter(Student.phone == phone).all()
    if len(id) > 0 or len(emails) > 0 or len(phones) > 0:
        print("this")
        return jsonify(code=400, msg="Some Information is invalid")
    else:
        return jsonify(code=200, msg="this Phone number is available")


@sysAdmin.route('/dormCheckID', methods=['GET', 'POST'])
def check_ID():
    stu_id = request.args.get('id')
    user = Student.query.filter(Student.stu_number == stu_id).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The id has already existed")
    else:
        return jsonify(code=200, msg="this phone number is available")


@sysAdmin.route('/dormCheckEmail', methods=['GET', 'POST'])
def check_email():
    email = request.args.get('email')
    user = Student.query.filter(Student.email == email).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The email has already existed")
    else:
        return jsonify(code=200, msg="this phone number is available")


@sysAdmin.route('/dormCheckPhone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    user = Student.query.filter(Student.phone == phone).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The Phone number has already existed")
    else:
        return jsonify(code=200, msg="this Phone number is available")


# guests CRUD ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@sysAdmin.route('/search_gue', methods=['GET', 'POST'])  # 路由名待完善核对
def search_gue():
    building_id = request.args.get('building_id', '0')
    key_word = request.args.get('content')
    tag = request.args.get('tag')
    pagenum = int(request.args.get('page', 1))
    enter_type = 'search'
    is_successful = request.args.get('isSuccessful', "True")  # The default value is True

    if building_id == '0':

        if tag == 'all':
            stu = Student.query.filter_by(stu_number=key_word).first()
            if stu:
                gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                       Guest.phone.contains(key_word),
                                                       Guest.stu_id == stu.id,
                                                       Guest.arrive_time.contains(key_word),
                                                       Guest.leave_time.contains(key_word),
                                                       )), Guest.is_deleted == False).paginate(page=pagenum, per_page=5)
            else:
                gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                       Guest.phone.contains(key_word),
                                                       Guest.arrive_time.contains(key_word),
                                                       Guest.leave_time.contains(key_word),
                                                       )), Guest.is_deleted == False).paginate(page=pagenum, per_page=5)

        elif tag == 'gue_name':
            gue_list = Guest.query.filter(and_(Guest.gue_name.contains(key_word), Guest.is_deleted == False)).paginate(
                page=pagenum, per_page=5)

        elif tag == 'stu_number':

            gue_list = Guest.query.join(Student).filter(
                and_(Student.stu_number == key_word, Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)

        elif tag == 'phone':
            gue_list = Guest.query.filter(and_(Guest.phone.contains(key_word), Guest.is_deleted == False)).paginate(
                page=pagenum, per_page=5)

        elif tag == 'has_left':
            gue_list = Guest.query.filter(and_(Guest.has_left == True, Guest.is_deleted == False)).paginate(
                page=pagenum, per_page=5)

        elif tag == 'has_not_left':
            gue_list = Guest.query.filter(and_(Guest.has_left == False, Guest.is_deleted == False)).paginate(
                page=pagenum, per_page=5)

    else:

        if tag == 'all':
            stu = Student.query.filter_by(stu_number=key_word).first()
            if stu:
                gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                       Guest.phone.contains(key_word),
                                                       Guest.stu_id == stu.id,
                                                       Guest.arrive_time.contains(key_word),
                                                       Guest.leave_time.contains(key_word),
                                                       ), Guest.is_deleted == False,
                                                   Guest.student.building_id == building_id)).paginate(page=pagenum,
                                                                                                       per_page=5)
            else:
                gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                       Guest.phone.contains(key_word),
                                                       Guest.arrive_time.contains(key_word),
                                                       Guest.leave_time.contains(key_word),
                                                       ), Guest.is_deleted == False,
                                                   Guest.student.building_id == building_id)).paginate(page=pagenum,
                                                                                                       per_page=5)

        elif tag == 'gue_name':
            gue_list = Guest.query.filter(and_(Guest.gue_name.contains(key_word), Guest.is_deleted == False,
                                               Guest.student.building_id == building_id)).paginate(
                page=pagenum, per_page=5)

        elif tag == 'stu_number':

            gue_list = Guest.query.join(Student).filter(
                and_(Student.stu_number == key_word, Guest.is_deleted == False,
                     Guest.student.building_id == building_id)).paginate(page=pagenum, per_page=5)

        elif tag == 'phone':
            gue_list = Guest.query.filter(and_(Guest.phone.contains(key_word), Guest.is_deleted == False,
                                               Guest.student.building_id == building_id)).paginate(
                page=pagenum, per_page=5)

        elif tag == 'has_left':
            gue_list = Guest.query.filter(and_(Guest.has_left == True, Guest.is_deleted == False,
                                               Guest.student.building_id == building_id)).paginate(
                page=pagenum, per_page=5)

        elif tag == 'has_not_left':
            gue_list = Guest.query.filter(and_(Guest.has_left == False, Guest.is_deleted == False,
                                               Guest.student.building_id == building_id)).paginate(
                page=pagenum, per_page=5)

    return render_template('samples/systemGuests.html', pagination=gue_list, enterType=enter_type, content=key_word,
                           tag=tag, isSuccessful=is_successful, function='guests')  # 待完善核对


#
# @sysAdmin.route('/delete_gue', endpoint='delete_gue')
# def delete_gue():
#     id = request.args.get('id')
#     content = request.args.get('content')
#     tag = request.args.get('tag')
#     enter_type = request.args.get('enterType')
#     page = request.args.get('page')
#
#     guest = Guest.query.get(id)
#     guest.is_deleted = True
#     db.session.add(guest)
#     db.session.commit()
#
#     if enter_type == "home":
#         return redirect(url_for('main.home_sys_admin_gue', page=page))
#     elif enter_type == "search":
#         return redirect(url_for('sysAdmin.search_gue', content=content, tag=tag, page=page))
#
#     return redirect(url_for('main.home_sys_admin_gue', page=page))  # 待完善核对

#
# @sysAdmin.route('/leave_gue', endpoint='leave_gue')
# def leave_gue():
#     id = request.args.get('id')
#     content = request.args.get('content')
#     tag = request.args.get('tag')
#     enter_type = request.args.get('enterType')
#     page = request.args.get('page')
#
#     guest = Guest.query.get(id)
#     guest.has_left = True
#     guest.leave_time = datetime.now()
#     db.session.add(guest)
#     db.session.commit()
#
#     if enter_type == "home":
#         return redirect(url_for('main.home_sys_admin_gue', page=page))
#     elif enter_type == "search":
#         return redirect(url_for('sysAdmin.search_gue', content=content, tag=tag, page=page))
#
#     return redirect(url_for('main.home_sys_admin_gue', page=page))  # 待完善核对

#
# @sysAdmin.route('/add_gue', methods=['GET', 'POST'])
# def add_gue():
#     if request.method == 'POST':
#         gue_name = request.form.get('gue_name')
#         stu_number = request.form.get('stu_number')
#         phone = request.form.get('phone')
#         note = request.form.get('note')
#
#         if gue_name != '' and phone != '' and stu_number != '':
#             student = Student.query.filter_by(stu_number=stu_number).first()
#             if student:
#                 if note != '':
#                     new_guest = Guest(gue_name=gue_name, phone=phone, stu_id=student.id)
#                 else:
#                     new_guest = Guest(gue_name=gue_name, phone=phone, stu_id=student.id, note=note)
#
#                 db.session.add(new_guest)
#                 db.session.commit()
#
#                 return redirect(url_for('main.home_sys_admin_gue', isSuccessful=True))
#             else:
#                 return redirect(url_for('main.home_sys_admin_gue', isSuccessful=False))
#         else:
#             return redirect(url_for('main.home_sys_admin_gue', isSuccessful=False))
#
#     return render_template('samples/guestRegister.html', function='guests')  # 待完善核对

#
# @sysAdmin.route('/update_gue', methods=['GET', 'POST'])
# def update_gue():
#     id = request.args.get('id')
#     guest = Guest.query.get(id)
#     content = request.args.get('content')
#     tag = request.args.get('tag')
#     enter_type = request.args.get('enterType')
#     page = request.args.get('page')
#     is_changed = False
#     is_stop = False  # 判断是否要停止当前修改，防止一部分信息被改，一部分没改
#
#     if request.method == 'POST':
#         gue_name = request.form.get('gue_name')
#         gue_stu_number = request.form.get('stu_number')  # 待核对
#         gue_phone = request.form.get('phone')
#
#         if gue_name != '':
#             guest.gue_name = gue_name
#             is_changed = True
#
#         if gue_stu_number != '':
#             if validate_gue_stu_number(gue_stu_number):
#                 student = Student.query.filter_by(stu_number=gue_stu_number).first()
#                 guest.stu_id = student.id
#                 is_changed = True
#             else:
#                 is_stop = True
#
#         if gue_phone != '':
#             if validate_gue_phone(gue_phone):
#                 guest.phone = gue_phone
#                 is_changed = True
#             else:
#                 is_stop = True
#
#         # 检查信息是否修改成功
#
#         if is_changed and not is_stop:
#             db.session.add(guest)
#             db.session.commit()
#
#             if enter_type == "home":
#                 return redirect(url_for('main.home_sys_admin_gue', page=page, isSuccessful="True"))
#             elif enter_type == "search":
#                 return redirect(
#                     url_for('sysAdmin.search_gue', content=content, tag=tag, page=page, isSuccessful="True"))
#         else:
#             if enter_type == "home":
#                 return redirect(url_for('main.home_sys_admin_gue', page=page, isSuccessful="False"))
#             elif enter_type == "search":
#                 return redirect(
#                     url_for('sysAdmin.search_gue', content=content, tag=tag, page=page, isSuccessful="False"))
#
#         return render_template('samples/guestRegister.html', function='guests')  # 待完善核对


def validate_gue_stu_number(n):
    if len(n) == 8:
        stu = Student.query.filter_by(stu_number=n).first()
        if stu:
            return True
        return False
    return False


def validate_gue_phone(p):
    if len(p) == 11:
        gue = Guest.query.filter_by(phone=p).first()
        if not gue:
            return True
        return False
    return False


@sysAdmin.route('/sysCheckGueStuid', methods=['GET', 'POST'])
def check_Gue_Stu_ID():
    stu_id = request.args.get('id')
    user = Student.query.filter(Student.stu_number == stu_id).all()
    if stu_id == "":
        return jsonify(code=200, msg="this phone number is available")
    print(len(user))
    if len(user) == 0:
        print("enter")
        return jsonify(code=400, msg="This ID doesn't Exist")
    else:
        return jsonify(code=200, msg="this phone number is available")


@sysAdmin.route('/sysCheckGueStuidAdd', methods=['GET', 'POST'])
def check_Gue_Stu_ID_Add():
    stu_id = request.args.get('id')
    phone = request.args.get('phone')
    gue_name = request.args.get('gue_name')
    user = Student.query.filter(Student.stu_number == stu_id).all()
    if stu_id == "" or gue_name == "" or phone == "":
        return jsonify(code=400, msg="Please fill the required information")
    print(len(user))
    if len(user) == 0:
        print("enter")
        return jsonify(code=400, msg="This ID doesn't Exist")
    else:
        return jsonify(code=200, msg="this phone number is available")


# dormitory administrator CRUD ------------------------------------------------------------------------------------------------------------


@sysAdmin.route('/search_da', methods=['GET', 'POST'])
def search_da():
    """
    fuzzy querying was used
    get a da_list that is a list of dormAdmin objects that meet the filter requirement
    """
    building_id = request.args.get('building_id', '0')

    key_word = request.args.get('content')
    tag = request.args.get('tag')
    pagenum = int(request.args.get('page', 1))
    enter_type = 'search'
    is_successful = request.args.get('isSuccessful', "True")  # The default value is True

    if building_id == '0':
        if tag == 'all':
            da_list = DAdmin.query.filter(and_(or_(DAdmin.da_name.contains(key_word),
                                                   DAdmin.da_number.contains(key_word),
                                                   DAdmin.phone.contains(key_word),
                                                   DAdmin.email.contains(key_word),
                                                   ), DAdmin.is_deleted == False)).order_by(
                DAdmin.building_id).paginate(page=pagenum, per_page=5)

        elif tag == 'da_name':
            da_list = DAdmin.query.filter(
                and_(DAdmin.da_name.contains(key_word), DAdmin.is_deleted == False)).order_by(
                DAdmin.building_id).paginate(page=pagenum, per_page=5)

        elif tag == 'da_number':
            da_list = DAdmin.query.filter(
                and_(DAdmin.da_number.contains(key_word), DAdmin.is_deleted == False)).order_by(
                DAdmin.building_id).paginate(page=pagenum, per_page=5)

        elif tag == 'phone':
            da_list = DAdmin.query.filter(
                and_(DAdmin.phone.contains(key_word), DAdmin.is_deleted == False)).order_by(
                DAdmin.building_id).paginate(page=pagenum, per_page=5)

        elif tag == 'email':
            da_list = DAdmin.query.filter(
                and_(DAdmin.email.contains(key_word), DAdmin.is_deleted == False)).order_by(
                DAdmin.building_id).paginate(page=pagenum, per_page=5)

    else:
        if tag == 'all':
            da_list = DAdmin.query.filter(
                and_(DAdmin.building_id == building_id, or_(DAdmin.da_name.contains(key_word),
                                                            DAdmin.da_number.contains(key_word),
                                                            DAdmin.phone.contains(key_word),
                                                            DAdmin.email.contains(key_word),
                                                            ), DAdmin.is_deleted == False)).order_by(
                DAdmin.building_id).paginate(page=pagenum, per_page=5)

        elif tag == 'da_name':
            da_list = DAdmin.query.filter(
                and_(DAdmin.da_name.contains(key_word), DAdmin.is_deleted == False,
                     DAdmin.building_id == building_id)).paginate(page=pagenum, per_page=5)

        elif tag == 'da_number':
            da_list = DAdmin.query.filter(
                and_(DAdmin.da_number.contains(key_word), DAdmin.is_deleted == False,
                     DAdmin.building_id == building_id)).paginate(page=pagenum, per_page=5)

        elif tag == 'phone':
            da_list = DAdmin.query.filter(
                and_(DAdmin.phone.contains(key_word), DAdmin.is_deleted == False,
                     DAdmin.building_id == building_id)).paginate(page=pagenum, per_page=5)

        elif tag == 'email':
            da_list = DAdmin.query.filter(
                and_(DAdmin.email.contains(key_word), DAdmin.is_deleted == False,
                     DAdmin.building_id == building_id)).paginate(page=pagenum, per_page=5)

    return render_template('.html', pagination=da_list, enterType=enter_type, content=key_word,
                           tag=tag, isSuccessful=is_successful, function='das')


# lost & found ---------------------------------------------------------------------------------------------------------------------


@sysAdmin.route("/lost_and_found_lost/lost")
def lost_and_found_lost():
    """
    The function for showing the lost information in the lost and found system
    """
    pagenum = int(request.args.get('page', 1))
    pagination = Lost.query.paginate(page=pagenum, per_page=5)
    return render_template("samples/studentLost.html", function="lost and found", pagination=pagination, pagenum=pagenum)     # 待核对


@sysAdmin.route("/lost_and_found_found/found")
def lost_and_found_found():
    """
    The function for showing the found information in the lost and found system
    """
    pagenum = int(request.args.get('page', 1))
    pagination = Found.query.paginate(page=pagenum, per_page=6)
    return render_template("samples/studentFound.html", function="lost and found", pagination=pagination, pagenum=pagenum)     # 待核对


@sysAdmin.route("/lost_and_found/details")
def lost_and_found_details():
    """
    The function for showing the detail page of the information in the lost and found system
    """
    # get the type of lost and found
    lnf_type = request.args.get('lnf_type')
    # according to the type of lost and found, get the according id
    if lnf_type == 'lost':
        lost_id = request.args.get('lost_id')

        # get the list of replies of this piece of information
        lost = Lost.query.filter_by(id=lost_id).first()
        reply_list = lost.replies

        return render_template("samples/lostDetail.html", function="lost and found", lnf_type=lnf_type, lost=lost,
                               reply_list=reply_list)       # 待核对

    elif lnf_type == 'found':
        found_id = request.args.get('found_id')

        # get the list of replies of this piece of information
        found = Found.query.filter_by(id=found_id).first()
        reply_list = found.replies

        return render_template("samples/foundDetail.html", function="lost and found", lnf_type=lnf_type, found=found,
                               reply_list=reply_list)       # 待核对
