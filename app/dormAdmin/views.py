from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import logout_user, login_required, login_user, current_user
from sqlalchemy import or_, and_, desc
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
                           tag=tag, isSuccessful=is_successful)


@dormAdmin.route('/delete_stu', endpoint='delete')
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
        return redirect(url_for('main.home_dorm_admin'))
    elif enter_type == "search":
        return redirect(url_for('dormAdmin.search_stu', content=content, tag=tag, page=page))

    return redirect(url_for('main.home_dorm_admin'))


@dormAdmin.route('/add_stu', methods=['GET', 'POST'])
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
                return redirect(url_for('main.home_dorm_admin', isSuccessful=True))
            else:
                return redirect(url_for('main.home_dorm_admin', isSuccessful=False))
        else:
            return redirect(url_for('main.home_dorm_admin', isSuccessful=False))

    return render_template('samples/testindex.html')


@dormAdmin.route('/update_stu', endpoint='update', methods=['GET', 'POST'])
def update_stu():
    id = request.args.get('id')
    student = Student.query.get(id)
    content = request.args.get('content')
    tag = request.args.get('tag')
    enter_type = request.args.get('enterType')
    page = request.args.get('page')
    is_changed = False

    if request.method == 'POST':
        stu_name = request.form.get('name')
        stu_number = request.form.get('stu_ID')
        print("stu_number length: " + str(len(stu_number)))
        phone = request.form.get('phone')
        email = request.form.get('email')
        room_number_str = request.form.get('room')
        room_number = None

        if room_number_str != '':
            room_number = int(room_number_str)

        if stu_name != '':
            student.stu_name = stu_name
            is_changed = True

        if stu_number != '':
            if validate_stu_number(stu_number):
                student.stu_number = stu_number
                is_changed = True

        if phone != '':
            if validate_phone(phone):
                student.phone = phone
                is_changed = True

        if email != '':
            if validate_email(email):
                student.email = email
                is_changed = True

        if room_number is not None:
            student.room_number = room_number
            is_changed = True

        # 检查信息是否修改成功
        if is_changed:
            db.session.add(student)
            db.session.commit()

            if enter_type == "home":
                return redirect(url_for('main.home_dorm_admin', isSuccessful="True"))
            elif enter_type == "search":
                return redirect(
                    url_for('dormAdmin.search_stu', content=content, tag=tag, page=page, isSuccessful="True"))
        else:
            if enter_type == "home":
                return redirect(url_for('main.home_dorm_admin', isSuccessful="False"))
            elif enter_type == "search":
                return redirect(
                    url_for('dormAdmin.search_stu', content=content, tag=tag, page=page, isSuccessful="False"))

    return render_template('samples/testindex.html')


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


@dormAdmin.route('/dormAdd', methods=['GET', 'POST'])
def check_add():
    stu_id = request.args.get('id')
    id = Student.query.filter(Student.stu_number == stu_id).all()
    email = request.args.get('email')
    emails = Student.query.filter(Student.email == email).all()
    phone = request.args.get('phone')
    phones = Student.query.filter(Student.phone == phone).all()
    print(id,phone,email)
    if stu_id =="" or email =="" or phone =="":
        return jsonify(code=400, msg="You have to fill all the Information")
    if len(id) > 0 or len(emails) > 0 or len(phones) > 0:
        return jsonify(code=400, msg="Some Information is invalid")
    else:
        return jsonify(code=200, msg="this Phone number is available")


@dormAdmin.route('/dormModify', methods=['GET', 'POST'])
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


@dormAdmin.route('/dormCheckID', methods=['GET', 'POST'])
def check_ID():
    stu_id = request.args.get('id')
    user = Student.query.filter(Student.stu_number == stu_id).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The id has already existed")
    else:
        return jsonify(code=200, msg="this phone number is available")


@dormAdmin.route('/dormCheckEmail', methods=['GET', 'POST'])
def check_email():
    email = request.args.get('email')
    user = Student.query.filter(Student.email == email).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The email has already existed")
    else:
        return jsonify(code=200, msg="this phone number is available")


@dormAdmin.route('/dormCheckPhone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    user = Student.query.filter(Student.phone == phone).all()
    if len(user) > 0:
        return jsonify(code=400, msg="The Phone number has already existed")
    else:
        return jsonify(code=200, msg="this Phone number is available")


# guests CRUD ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@dormAdmin.route('/search_gue', methods=['GET', 'POST'])  # 路由名待完善核对
def search_gue():
    key_word = request.args.get('content')
    tag = request.args.get('tag')
    pagenum = int(request.args.get('page', 1))
    enter_type = 'search'

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
                                                   )), Guest.is_deleted == False).paginate(page=pagenum, per_page=5)
        else:
            gue_list = Guest.query.filter(and_(or_(Guest.gue_name.contains(key_word),
                                                   Guest.phone.contains(key_word),
                                                   Guest.room_number == key_word,
                                                   Guest.building_id == key_word,
                                                   Guest.arrive_time.contains(key_word),
                                                   Guest.leave_time.contains(key_word),
                                                   )), Guest.is_deleted == False).paginate(page=pagenum, per_page=5)

    elif tag == 'gue_name':
        gue_list = Guest.query.filter(and_(Guest.stu_name.contains(key_word), Guest.is_deleted == False)).paginate(
            page=pagenum, per_page=5)

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


@dormAdmin.route('/add_gue', methods=['GET', 'POST'])
def add_gue():
    if request.method == 'POST':
        gue_name = request.form.get('gue_name')
        gue_stu_number = request.form.get('gue_stu_number')
        gue_phone = request.form.get('gue_phone')
        gue_college = request.form.get('gue_college')
        gue_building_id = int(request.form.get('gue_building_id'))
        gue_room_number = int(request.form.get('gue_room_number'))
        arrive_time = request.form.get('arrive_time')
        leave_time = request.form.get('leave_time')

        new_guest = Guest(gue_name=gue_name, gue_stu_number=gue_stu_number, gue_phone=gue_phone,
                          gue_college=gue_college,
                          gue_building_id=gue_building_id, gue_room_number=gue_room_number, arrive_time=arrive_time,
                          leave_time=leave_time)
        db.session.add(new_guest)
        db.session.commit()

    return render_template('main.home_dorm_admin')  # 待完善核对
