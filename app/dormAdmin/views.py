from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import logout_user, login_required, login_user, current_user
from sqlalchemy import or_, and_
from wtforms import ValidationError
from . import dormAdmin
from .. import db
from ..models import Student, Guest


# students CRUD ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@dormAdmin.route('/search_stu', methods=['GET', 'POST'])
def search_stu():
    """
    fuzzy querying was used
    :return: stu_list ab list of Student objects that meet the filter requirement
    """
    key_word = request.args.get('content')
    tag = request.args.get('tag')

    # print('tag: ' + tag)
    # print('key_word:' + key_word)

    stu_list = []
    if tag == 'all':
        stu_list = Student.query.filter(and_(or_(Student.stu_name.contains(key_word),
                                                 Student.stu_number.contains(key_word),
                                                 Student.phone.contains(key_word),
                                                 Student.college.contains(key_word),
                                                 Student.room_number.contains(key_word),
                                                 Student.enroll_date.contains(key_word)
                                                 )), Student.is_deleted == False).all()

    elif tag == 'stu_name':
        stu_list = Student.query.filter(and_(Student.stu_name.contains(key_word), Student.is_deleted == False)).all()

    elif tag == 'stu_number':
        stu_list = Student.query.filter(and_(Student.stu_number.contains(key_word), Student.is_deleted == False)).all()

    elif tag == 'phone':
        stu_list = Student.query.filter(and_(Student.phone.contains(key_word), Student.is_deleted == False)).all()

    elif tag == 'college':
        stu_list = Student.query.filter(and_(Student.college.contains(key_word), Student.is_deleted == False)).all()

    elif tag == 'room_number':
        stu_list = Student.query.filter(and_(Student.room_number.contains(key_word), Student.is_deleted == False)).all()

    elif tag == 'enroll_date':
        stu_list = Student.query.filter(and_(Student.enroll_date.contains(key_word), Student.is_deleted == False)).all()

    # print(stu_list)
    return render_template('samples/testindex.html', students=stu_list)  # 待完善核对


@dormAdmin.route('/delete_stu', endpoint='delete')
def delete_stu():
    id = request.args.get('id')
    student = Student.query.get(id)
    student.is_deleted = True
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('main.home_dorm_admin'))  # 待完善核对


@dormAdmin.route('/add_stu', methods=['GET', 'POST'])
def add_stu():
    if request.method == 'POST':
        stu_name = request.form.get('stu_name')
        stu_number = request.form.get('stu_number')
        phone = request.form.get('phone')
        college = request.form.get('college')
        building_id = int(request.form.get('building_id'))
        room_number = int(request.form.get('room_number'))
        new_student = Student(stu_name=stu_name, stu_number=stu_number, phone=phone, college=college,
                              building_id=building_id, room_number=room_number)
        db.session.add(new_student)
        db.session.commit()

    return render_template('main.home_dorm_admin')  # 待完善核对


# @dormAdmin.route('/update_stu', endpoint='update', method=['GET', 'POST'])  # 路由名待完善核对
# def update_stu():
#     if request.method == 'POST':
#         id = request.form.get('id')
#         stu_ID = request.form.get('stu_ID')
#         phone = request.form.get('phone')
#         name = request.form.get('name')
#         room = request.form.get('room')
#         email = request.form.get('email')
#         user = Student.query.get(id)
#         user.stu_ID = stu_ID
#         user.phone = phone
#         user.name = name
#         user.room = room
#         user.email = email
#         db.session.commit()
#         return redirect(url_for('main.home_dorm_admin'))  # 路由名待完善核对
#
#     else:
#         id = request.args.get('id')
#         user = User.query.get(id)
#         return render_template('user/update.html', user=user)  # 路由名待完善核对


@dormAdmin.route('/update_stu', endpoint='update', methods=['GET', 'POST'])  # 路由名待完善核对
def update_stu():
    id = request.args.get('id')
    student = Student.query.get(id)

    if request.method == 'POST':
        stu_name = request.form.get('name')
        stu_number = request.form.get('stu_ID')
        phone = request.form.get('phone')
        email = request.form.get('email')
        room_number = int(request.form.get('room'))

        if validate_stu_number(stu_number) and validate_phone(phone) and validate_email(email):
            student.stu_name = stu_name
            student.stu_number = stu_number
            student.phone = phone
            student.email = email
            student.room_number = room_number
            db.session.add(student)
            db.session.commit()

        return redirect(url_for('main.home_dorm_admin'))  # 路由名待完善核对

    return render_template('samples/testindex.html')  # 路由名待完善核对


def validate_stu_number(n):
    """
    Verify if the student number has not been used.
    :param n:   student number
    """
    stu = Student.query.filter_by(stu_number=n).first()
    if stu:
        if not stu.is_deleted:
            return False
        return True
    return True


def validate_phone(p):
    """
    Verify if the phone number has not been used.
    :param p:   phone number
    """
    stu = Student.query.filter_by(phone=p).first()
    if stu:
        if not stu.is_deleted:
            return False
        return True
    return True


def validate_email(e):
    """
    Verify if the email has not been used.
    :param e:   email
    """
    stu = Student.query.filter_by(email=e).first()
    if stu:
        if not stu.is_deleted:
            return False
        return True
    return True


# guests CRUD ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@dormAdmin.route('/search_gue', methods=['GET', 'POST'])  # 路由名待完善核对
def search_gue():
    key_word = request.args.get('key_word')  # 待完善核对
    tag = request.args.get('tag')  # 待完善核对

    if tag == 'all':
        stu = Student.query.filter_by(stu_number=key_word).first()
        if stu:
            gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                   Guest.phone.contains(key_word),
                                                   Guest.stu_id == stu.id,
                                                   Guest.room_number == key_word,
                                                   Guest.building_id == key_word,
                                                   Guest.arrive_time.contains(key_word),
                                                   Guest.leave_time.contains(key_word),
                                                   )), Guest.is_deleted == False).all()
        else:
            gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                   Guest.phone.contains(key_word),
                                                   Guest.room_number == key_word,
                                                   Guest.building_id == key_word,
                                                   Guest.arrive_time.contains(key_word),
                                                   Guest.leave_time.contains(key_word),
                                                   )), Guest.is_deleted == False).all()

    elif tag == 'gue_name':
        gue_list = Guest.query.filter(and_(Guest.stu_name.contains(key_word), Guest.is_deleted == False)).all()

    elif tag == 'stu_number':
        ref_stu_list = Student.query.filter(Student.stu_number.contains(key_word)).all()
        gue_list = []
        for stu in ref_stu_list:
            gue = Guest.query.filter(and_(Guest.stu_id == stu.id, Guest.is_deleted == False)).first()
            if gue:
                gue_list.append(gue)

    elif tag == 'phone':
        gue_list = Guest.query.filter(and_(Guest.phone.contains(key_word), Guest.is_deleted == False)).all()

    elif tag == 'relation':
        gue_list = Guest.query.filter(and_(Guest.relation.contains(key_word), Guest.is_deleted == False)).all()

    elif tag == 'building_id':
        gue_list = Guest.query.filter(and_(Guest.building_id == key_word, Guest.is_deleted == False)).all()

    elif tag == 'room_number':
        gue_list = Guest.query.filter(and_(Guest.room_number == key_word, Guest.is_deleted == False)).all()

    elif tag == 'arrive_time':
        gue_list = Guest.query.filter(and_(Guest.arrive_time.contains(key_word), Guest.is_deleted == False)).all()

    elif tag == 'leave_time':
        gue_list = Guest.query.filter(and_(Guest.leave_time.contains(key_word), Guest.is_deleted == False)).all()

    return render_template('.html', gue_list=gue_list)  # 待完善核对
