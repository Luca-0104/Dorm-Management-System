from flask import render_template, flash, redirect, url_for, request, jsonify
from sqlalchemy import or_, and_
from wtforms import ValidationError

from . import dormAdmin
from ..models import Student
from flask_login import logout_user, login_required, login_user, current_user


@dormAdmin.route('/search', methods=['GET', 'POST'])  # 路由名待完善核对
def search():
    """
    fuzzy querying was used
    :return: stu_list ab list of Student objects that meet the filter requirement
    """
    key_word = request.args.get('search')  # 待完善核对
    tag = request.form.get('tag')  # 待完善核对

    if tag == 'all':
        stu_list = Student.query.filter(and_(or_(Student.stu_name.contains(key_word),
                                                 Student.stu_number == key_word,
                                                 Student.phone.contains(key_word),
                                                 Student.college.contains(key_word),
                                                 Student.room_number == key_word,
                                                 Student.enroll_date.contains(key_word)
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
        stu_list = Student.query.filter(and_(Student.room_number.contains(key_word), not Student.is_deleted)).all()

    elif tag == 'enroll_date':
        stu_list = Student.query.filter(and_(Student.enroll_date.contains(key_word), not Student.is_deleted)).all()

    return render_template('.html', stu_list=stu_list)  # 待完善核对


@dormAdmin.route('/delete', endpoint='delete')
def delete():
    id = request.args.get('id')
    student = Student.query.get(id)
    student.is_deleted = True
    db.session.commit()
    return redirect(url_for('dormAdmin.home'))  # 待完善核对
from flask import render_template, redirect, request



@dormAdmin.route ('/student/list')
def student_list():
    items = db.session.query(Student).limit(20)
    return render_template('dormAdmin.home', items=items)

@dormAdmin.route ('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        stu_wor_id = request.form.get('stu_wor_id')
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        room_number = int(request.form.get('room_number'))
        student = Student(stu_wor_id=stu_wor_id, username=username, phone=phone, email=email, room_number=room_number)
        db.session.add(student)
        db.session.commit()
        return render_template('dormAdmin.home')






