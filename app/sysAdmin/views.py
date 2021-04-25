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