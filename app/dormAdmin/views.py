from flask import render_template, redirect, request


from . import dormAdmin
from .. import db

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






