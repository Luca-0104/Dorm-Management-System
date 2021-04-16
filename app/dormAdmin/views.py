from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import logout_user, login_required, login_user, current_user
from sqlalchemy import or_, and_
from wtforms import ValidationError
from . import dormAdmin
from .. import db
from ..models import Student, Guest


# students CRUD ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@dormAdmin.route('/search_stu', methods=['GET', 'POST'])  # 路由名待完善核对
def search_stu():
    """
    fuzzy querying was used
    :return: stu_list ab list of Student objects that meet the filter requirement
    """
    return "yes"
    key_word = request.args.get('search')  # 待完善核对
    tag = request.form.get('tag')  # 待完善核对

    if tag == 'all':
        stu_list = Student.query.filter(and_(or_(Student.stu_name.contains(key_word),
                                                 Student.stu_number == key_word,
                                                 Student.phone.contains(key_word),
                                                 Student.college.contains(key_word),
                                                 str(Student.room_number) == key_word,
                                                 str(Student.enroll_date).contains(key_word)
                                                 )), not Student.is_deleted).all()

    elif tag == 'stu_name':
        stu_list = Student.query.filter(and_(Student.stu_name.contains(key_word), not Student.is_deleted)).all()

    elif tag == 'stu_number':
        stu_list = Student.query.filter(and_(Student.stu_number.contains(key_word), not Student.is_deleted)).all()

    elif tag == 'phone':
        stu_list = Student.query.filter(and_(Student.phone.contains(key_word), not Student.is_deleted)).all()

    elif tag == 'college':
        stu_list = Student.query.filter(and_(Student.college.contains(key_word), not Student.is_deleted)).all()

    elif tag == 'room_number':
        stu_list = Student.query.filter(and_(str(Student.room_number).contains(key_word), not Student.is_deleted)).all()

    elif tag == 'enroll_date':
        stu_list = Student.query.filter(and_(str(Student.enroll_date).contains(key_word), not Student.is_deleted)).all()

    return render_template('../templates/samples/testindex.html', stu_list=stu_list)  # 待完善核对


@dormAdmin.route('/delete_stu', endpoint='delete')
def delete_stu():
    id = request.args.get('id')
    student = Student.query.get(id)
    student.is_deleted = True
    db.session.commit()
    return redirect(url_for('auth.home'))  # 待完善核对


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

    return render_template('auth.home')  # 待完善核对


# guests CRUD ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@dormAdmin.route('/search_gue', methods=['GET', 'POST'])  # 路由名待完善核对
def search_gue():
    key_word = request.args.get('key_word')  # 待完善核对
    tag = request.form.get('tag')  # 待完善核对

    if tag == 'all':
        stu = Student.query.filter_by(stu_number=key_word).first()
        if stu:
            gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                   Guest.phone.contains(key_word),
                                                   Guest.stu_id == stu.id,
                                                   str(Guest.room_number) == key_word,
                                                   str(Guest.building_id) == key_word,
                                                   str(Guest.arrive_time).contains(key_word),
                                                   str(Guest.leave_time).contains(key_word),
                                                   )), not Guest.is_deleted).all()
        else:
            gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                   Guest.phone.contains(key_word),
                                                   str(Guest.room_number) == key_word,
                                                   str(Guest.building_id) == key_word,
                                                   str(Guest.arrive_time).contains(key_word),
                                                   str(Guest.leave_time).contains(key_word),
                                                   )), not Guest.is_deleted).all()

    elif tag == 'gue_name':
        gue_list = Guest.query.filter(and_(Guest.stu_name.contains(key_word), not Guest.is_deleted)).all()

    elif tag == 'stu_number':
        ref_stu_list = Student.query.filter(Student.stu_number.contains(key_word)).all()
        gue_list = []
        for stu in ref_stu_list:
            gue = Guest.query.filter(and_(Guest.stu_id == stu.id, not Guest.is_deleted)).first()
            if gue:
                gue_list.append(gue)

    elif tag == 'phone':
        gue_list = Guest.query.filter(and_(Guest.phone.contains(key_word), not Guest.is_deleted)).all()

    elif tag == 'relation':
        gue_list = Guest.query.filter(and_(Guest.relation.contains(key_word), not Guest.is_deleted)).all()

    elif tag == 'building_id':
        gue_list = Guest.query.filter(and_(str(Guest.building_id) == key_word, not Guest.is_deleted)).all()

    elif tag == 'room_number':
        gue_list = Guest.query.filter(and_(str(Guest.room_number) == key_word, not Guest.is_deleted)).all()

    elif tag == 'arrive_time':
        gue_list = Guest.query.filter(and_(str(Guest.arrive_time).contains(key_word), not Guest.is_deleted)).all()

    elif tag == 'leave_time':
        gue_list = Guest.query.filter(and_(str(Guest.leave_time).contains(key_word), not Guest.is_deleted)).all()

    return render_template('.html', gue_list=gue_list)  # 待完善核对
