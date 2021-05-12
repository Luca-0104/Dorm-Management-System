from flask import request, render_template, redirect, url_for
from flask_login import current_user

from . import student
from .. import db
from ..models import Student, Repair, ReplyComplain, ReplyRepair, Complain, DAdmin, Notification


@student.route('/stu_reply', methods=['GET', 'POST'])
def stu_reply():
    """
    The function for replying the message (stu --> da)
    """
    author_id = current_user.id
    reply_type = request.args.get('reply_type')
    if reply_type == 'complain':
        complain_id = request.args.get('complain_id')
    elif reply_type == 'repair':
        repair_id = request.args.get('repair_id')

    if request.method == 'POST':
        content = request.form.get('content')
        if reply_type == 'complain':
            new_reply = ReplyComplain(content=content, complain_id=complain_id, auth_id=author_id)
        elif reply_type == 'repair':
            new_reply = ReplyRepair(content=content, repair_id=repair_id, auth_id=author_id)
        db.session.add(new_reply)
        db.session.commit()

    if reply_type == 'complain':
        return redirect(url_for('student.message_details', message_type='complain', complain_id=complain_id))
    elif reply_type == 'repair':
        return redirect(url_for('student.message_details', message_type='repair', repair_id=repair_id))


@student.route('/add_complain', methods=['GET', 'POST'])
def add_complain():
    """
    The function for adding new complain information
    """
    if request.method == 'POST':
        detail = request.form.get('detail')
        stu_num = current_user.stu_wor_id
        stu = Student.query.filter_by(stu_number=stu_num).first()
        stu_id = stu.id

        if detail != '' and stu_id is not None:
            # Add complain information into the complain table
            new_complain = Complain(detail=detail, stu_id=stu_id)
            db.session.add(new_complain)
            db.session.commit()

    return redirect(url_for('main.home_stu_complain'))


@student.route('/add_repair', methods=['GET', 'POST'])
def add_repair():
    """
    The function for adding new repair information
    """
    if request.method == 'POST':
        item = request.form.get('item')
        detail = request.form.get('detail')
        stu_num = current_user.stu_wor_id
        stu = Student.query.filter_by(stu_number=stu_num).first()
        stu_id = stu.id

        if item != '' and detail != '' and stu_id is not None:
            # Add repair information into the Repair table
            new_repair = Repair(item=item, detail=detail, stu_id=stu_id)
            db.session.add(new_repair)
            db.session.commit()

    return redirect(url_for('main.home_stu_repair'))
    # return render_template("samples/studentRepair.html", function="repair")


@student.route("/home_stu_message/repair")
def message_repair():
    """
    The function for showing the repair information in the message system
    """
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    stu_id = stu.id
    repair_list = Repair.query.filter_by(stu_id=stu_id).all()
    return render_template("samples/messageRepair.html", function="message", repair_list=repair_list)


@student.route("/home_stu_message/complain")
def message_complain():
    """
    The function for showing the complain information in the message system
    """
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    stu_id = stu.id
    complain_list = Complain.query.filter_by(stu_id=stu_id).all()
    return render_template("samples/messageComplain.html", function="message", complain_list=complain_list)


@student.route("/home_stu_message/notification")
def message_notification():
    """
    The function for showing the notification information in the message system
    Only show the notification that are published by the dorm administrator of this building
    """

    # find a list of dormitory administrators who in charge of the building of this student
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    building_id = stu.building_id
    da_list = DAdmin.query.filter_by(building_id=building_id).all()

    # create a list, which contains all the notification objects of each dormAdmin of this building
    notification_list = []
    for da in da_list:
        notifications = da.notifications
        for n in notifications:
            notification_list.append(n)
    for i in notification_list:
        print(i.time)
    return render_template("samples/messageNotification.html", function="message", notification_list=notification_list)


@student.route("/home_stu_message/details")
def message_details():
    """
    The function for showing the detail page
    """
    # get the type of message
    message_type = request.args.get('message_type')

    # according to the type of message, get the according id
    if message_type == 'repair':
        repair_id = request.args.get('repair_id')

        # get the list of replies of this piece of message
        repair = Repair.query.filter_by(id=repair_id).first()
        reply_list = repair.replies

        # 待考究：是传一个repair_id还是一个repair对象好？complain和notification亦然
        return render_template("samples/Message.html", function="message", message_type=message_type, repair=repair, reply_list=reply_list)

    elif message_type == 'complain':
        complain_id = request.args.get('complain_id')

        # get the list of replies of this piece of message
        complain = Complain.query.filter_by(id=complain_id).first()
        reply_list = complain.replies

        return render_template("samples/Message.html", function="message", message_type=message_type, complain=complain, reply_list=reply_list)

    elif message_type == 'notification':
        notification_id = request.args.get('notification_id')
        notification = Notification.query.filter_by(id=notification_id).first()
        return render_template("samples/Message.html", function="message", message_type=message_type, notification=notification)

    return render_template("samples/Message.html", function="message")


@student.route("/home_stu_change", methods=['GET','POST'])
def user_change():
    if request.method == "post":
        icon = request.files.get('icon')
        print(icon)
    return render_template('samples/studentIndex.html',function="index")