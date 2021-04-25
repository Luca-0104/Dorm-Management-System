from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import logout_user, login_required, login_user, current_user
from sqlalchemy import or_, and_, desc
from wtforms import ValidationError
from . import sysAdmin
from .. import db
from ..models import Student, Guest

@sysAdmin.route('/add_stu', methods=['GET', 'POST'])
def add_stu():
    if request.method == 'POST':
        stu_name = request.form.get('name')
        stu_number = request.form.get('stu_ID')
        phone = request.form.get('phone')
        email = request.form.get('email')
        college = request.form.get('college')
        # building_id_str = request.form.get('building_id')
        room_number_str = request.form.get('room')
        # building_id = None
        building_id = 1  # 暂时默认都给1，sprint3会将其改为宿管对应的楼号
        room_number = None

        # if building_id_str != '':
        #     building_id = int(building_id_str)

        if room_number_str != '':
            room_number = int(room_number_str)

        if stu_name != '' and stu_number != '' and phone != '' and email != '' and college != '' and building_id is not None and room_number is not None:
            if validate_stu_number(stu_number) and validate_phone(phone) and validate_email(email):
                new_student = Student(stu_name=stu_name,
                                      stu_number=stu_number,
                                      phone=phone,
                                      email=email,
                                      college=college,
                                      building_id=building_id,
                                      room_number=room_number)
                db.session.add(new_student)
                db.session.commit()
                return redirect(url_for('main.home_sys_admin', isSuccessful=True))
            else:
                return redirect(url_for('main.home_sys_admin', isSuccessful=False))
        else:
            return redirect(url_for('main.home_sys_admin', isSuccessful=False))

    return render_template('samples/testindex.html', function='students')


@sysAdmin.route('/search_stu', methods=['GET', 'POST'])
def search_stu():
    """
    fuzzy querying was used
    :return: stu_list ab list of Student objects that meet the filter requirement
    """
    key_word = request.args.get('content')
    tag = request.args.get('tag')
    pagenum = int(request.args.get('page', 1))
    enter_type = 'search'
    is_successful = request.args.get('isSuccessful', "True")  # The default value is True

    # print('tag: ' + tag)
    # print('key_word:' + key_word)

    stu_list = []
    if tag == 'all':
        stu_list = Student.query.filter(and_(or_(Student.stu_name.contains(key_word),
                                                 Student.stu_number.contains(key_word),
                                                 Student.phone.contains(key_word),
                                                 Student.college.contains(key_word),
                                                 Student.room_number.contains(key_word),
                                                 # Student.enroll_date.contains(key_word)
                                                 )), Student.is_deleted == False).order_by(
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
        stu_list = Student.query.filter(and_(Student.phone.contains(key_word), Student.is_deleted == False)).order_by(
            Student.room_number).paginate(page=pagenum, per_page=5)

    elif tag == 'college':
        stu_list = Student.query.filter(and_(Student.college.contains(key_word), Student.is_deleted == False)).order_by(
            Student.room_number).paginate(page=pagenum, per_page=5)

    elif tag == 'room_number':
        stu_list = Student.query.filter(
            and_(Student.room_number.contains(key_word), Student.is_deleted == False)).order_by(
            Student.room_number).paginate(page=pagenum, per_page=5)

    # elif tag == 'enroll_date':
    #     stu_list = Student.query.filter(and_(Student.enroll_date.contains(key_word), Student.is_deleted == False)).order_by(Student.room_number).paginate(page=pagenum, per_page=5)

    # print(stu_list)
    return render_template('samples/testindex.html', pagination=stu_list, enterType=enter_type, content=key_word,
                           tag=tag, isSuccessful=is_successful, function='students')



@sysAdmin.route('/delete_stu', endpoint='delete')
def delete_stu():
    id = request.args.get('id')
    content = request.args.get('content')
    tag = request.args.get('tag')
    enter_type = request.args.get('enterType')
    page = request.args.get('page')

    student = Student.query.get(id)
    student.is_deleted = True
    db.session.add(student)
    db.session.commit()

    if enter_type == "home":
        return redirect(url_for('main.home_sys_admin', page=page))
    elif enter_type == "search":
        return redirect(url_for('sysAdmin.search_stu', content=content, tag=tag, page=page))

    return redirect(url_for('main.home_sys_admin', page=page))