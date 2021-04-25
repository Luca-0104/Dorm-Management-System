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

@sysAdmin.route('/search_gue', methods=['GET', 'POST'])  # 路由名待完善核对
def search_gue():
    key_word = request.args.get('content')
    tag = request.args.get('tag')
    pagenum = int(request.args.get('page', 1))
    enter_type = 'search'
    is_successful = request.args.get('isSuccessful', "True")  # The default value is True

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
        gue_list = Guest.query.filter(and_(Guest.gue_name.contains(key_word), Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)

    elif tag == 'stu_number':

        gue_list = Guest.query.join(Student).filter(and_(Student.stu_number == key_word, Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)
        # ref_stu_list = Student.query.filter(Student.stu_number.contains(key_word)).all()
        # gue_list = []
        # for stu in ref_stu_list:
        #     gue = Guest.query.filter(and_(Guest.stu_id == stu.id, Guest.is_deleted == False)).first()
        #     if gue:
        #         gue_list.append(gue)

    elif tag == 'phone':
        gue_list = Guest.query.filter(and_(Guest.phone.contains(key_word), Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)

    elif tag == 'has_left':
        gue_list = Guest.query.filter(and_(Guest.has_left == True, Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)

    elif tag == 'has_not_left':
        gue_list = Guest.query.filter(and_(Guest.has_left == False, Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)

    # elif tag == 'arrive_time':
    #     gue_list = Guest.query.filter(and_(Guest.arrive_time.contains(key_word), Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)
    #
    # elif tag == 'leave_time':
    #     gue_list = Guest.query.filter(and_(Guest.leave_time.contains(key_word), Guest.is_deleted == False)).paginate(page=pagenum, per_page=5)

    return render_template('samples/guestRegister.html', pagination=gue_list, enterType=enter_type, content=key_word,
                           tag=tag, isSuccessful=is_successful, function='guests')  # 待完善核对

@sysAdmin.route('/add_gue', methods=['GET', 'POST'])
def add_gue():
    if request.method == 'POST':
        gue_name = request.form.get('gue_name')
        stu_number = request.form.get('stu_number')
        phone = request.form.get('phone')
        note = request.form.get('note')

        if gue_name != '' and phone != '' and stu_number != '':
            student = Student.query.filter_by(stu_number=stu_number).first()
            if student:
                if note != '':
                    new_guest = Guest(gue_name=gue_name, phone=phone, stu_id=student.id)
                else:
                    new_guest = Guest(gue_name=gue_name, phone=phone, stu_id=student.id, note=note)

                db.session.add(new_guest)
                db.session.commit()

                return redirect(url_for('main.home_dorm_admin_gue', isSuccessful=True))
            else:
                return redirect(url_for('main.home_dorm_admin_gue', isSuccessful=False))
        else:
            return redirect(url_for('main.home_dorm_admin_gue', isSuccessful=False))

    return render_template('samples/guestRegister.html', function='guests')  # 待完善核对

@sysAdmin.route('/delete_gue', endpoint='delete_gue')
def delete_gue():
    id = request.args.get('id')
    content = request.args.get('content')
    tag = request.args.get('tag')
    enter_type = request.args.get('enterType')
    page = request.args.get('page')

    guest = Guest.query.get(id)
    guest.is_deleted = True
    db.session.add(guest)
    db.session.commit()

    if enter_type == "home":
        return redirect(url_for('main.home_dorm_admin_gue', page=page))
    elif enter_type == "search":
        return redirect(url_for('dormAdmin.search_gue', content=content, tag=tag, page=page))

    return redirect(url_for('main.home_dorm_admin_gue', page=page))  # 待完善核对

@sysAdmin.route('/update_gue', methods=['GET', 'POST'])
def update_gue():
    id = request.args.get('id')
    guest = Guest.query.get(id)
    content = request.args.get('content')
    tag = request.args.get('tag')
    enter_type = request.args.get('enterType')
    page = request.args.get('page')
    is_changed = False
    is_stop = False  # 判断是否要停止当前修改，防止一部分信息被改，一部分没改

    if request.method == 'POST':
        gue_name = request.form.get('gue_name')
        gue_stu_number = request.form.get('stu_number')  # 待核对
        gue_phone = request.form.get('phone')

        if gue_name != '':
            guest.gue_name = gue_name
            is_changed = True

        if gue_stu_number != '':
            if validate_gue_stu_number(gue_stu_number):
                student = Student.query.filter_by(stu_number=gue_stu_number).first()
                guest.stu_id = student.id
                is_changed = True
            else:
                is_stop = True

        if gue_phone != '':
            if validate_gue_phone(gue_phone):
                guest.phone = gue_phone
                is_changed = True
            else:
                is_stop = True

        # 检查信息是否修改成功

        if is_changed and not is_stop:
            db.session.add(guest)
            db.session.commit()

            if enter_type == "home":
                return redirect(url_for('main.home_dorm_admin_gue', page=page, isSuccessful="True"))
            elif enter_type == "search":
                return redirect(
                    url_for('dormAdmin.search_gue', content=content, tag=tag, page=page, isSuccessful="True"))
        else:
            if enter_type == "home":
                return redirect(url_for('main.home_dorm_admin_gue', page=page, isSuccessful="False"))
            elif enter_type == "search":
                return redirect(
                    url_for('dormAdmin.search_gue', content=content, tag=tag, page=page, isSuccessful="False"))

        return render_template('samples/guestRegister.html', function='guests')  # 待完善核对
