import os

from flask import request, render_template, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from config import Config
from . import student
from .. import db
from ..models import Student, Repair, ReplyComplain, ReplyRepair, Complain, DAdmin, Notification, Lost, Found, \
    ReplyFound, ReplyLost

# The allowed extension type of the picture that is uploaded
ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp']


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
    elif reply_type == 'lost':
        lost_id = request.args.get('lost_id')
    elif reply_type == 'found':
        found_id = request.args.get('found_id')

    if request.method == 'POST':
        content = request.form.get('content')

        if reply_type == 'complain':
            new_reply = ReplyComplain(content=content, complain_id=complain_id, auth_id=author_id)
        elif reply_type == 'repair':
            new_reply = ReplyRepair(content=content, repair_id=repair_id, auth_id=author_id)
        elif reply_type == 'lost':
            new_reply = ReplyLost(content=content, lost_id=lost_id, auth_id=author_id)
        elif reply_type == 'found':
            new_reply = ReplyFound(content=content, found_id=found_id, auth_id=author_id)

        db.session.add(new_reply)
        db.session.commit()

    if reply_type == 'complain':
        return redirect(url_for('student.message_details', message_type='complain', complain_id=complain_id))
    elif reply_type == 'repair':
        return redirect(url_for('student.message_details', message_type='repair', repair_id=repair_id))
    elif reply_type == 'lost':
        return redirect(url_for('student.lost_and_found_details', lnf_type='lost', lost_id=lost_id))
    elif reply_type == 'found':
        return redirect(url_for('student.lost_and_found_details', lnf_type='found', found_id=found_id))


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


@student.route('/add_lost', methods=['GET', 'POST'])
def add_lost():
    """
    The function for adding new lost things' information
    """
    if request.method == 'POST':

        item = request.form.get('item')
        price = request.form.get('price')
        place = request.form.get('place')           # able to be blank
        lost_time = request.form.get('lost_time')   # able to be blank
        detail = request.form.get('detail')         # able to be blank

        stu_num = current_user.stu_wor_id
        stu = Student.query.filter_by(stu_number=stu_num).first()
        stu_id = stu.id

        if item != '' and stu_id is not None:
            # Add the information of the lost item into the Lost table
            if place == '' and lost_time == '' and detail == '':
                new_lost = Lost(item=item, price=price, stu_id=stu_id)

            elif place == '' and lost_time == '':
                new_lost = Lost(item=item, price=price, detail=detail, stu_id=stu_id)

            elif place == '' and detail == '':
                new_lost = Lost(item=item, price=price, stu_id=stu_id, lost_time=lost_time)

            elif lost_time == '' and detail == '':
                new_lost = Lost(item=item, price=price, stu_id=stu_id, place=place)

            else:
                new_lost = Lost(item=item, price=price, detail=detail, stu_id=stu_id, place=place, lost_time=lost_time)

            db.session.add(new_lost)
            db.session.commit()

    return redirect(url_for('main.home_stu_lost'))


@student.route('/add_found', methods=['GET', 'POST'])
def add_found():
    """
    The function for adding new found things' information
    """
    if request.method == 'POST':

        item = request.form.get('item')
        place = request.form.get('place')
        found_time = request.form.get('found_time')
        detail = request.form.get('detail')     # able to be blank
        icon = request.files.get('icon')        # able to be blank in the database, but we will not allow this happens

        stu_num = current_user.stu_wor_id
        stu = Student.query.filter_by(stu_number=stu_num).first()
        stu_id = stu.id

        icon_name = icon.filename
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name)
            file_path = os.path.join(Config.found_dir, icon_name).replace('\\', '/')
            icon.save(file_path)

        else:
            return redirect(url_for('main.home_stu_found'))

        if item != '' and stu_id is not None:
            # Add the information of the found item into the Found table
            path = 'upload/found'
            pic = os.path.join(path, icon_name).replace('\\', '/')

            if detail == '':
                new_found = Found(item=item, place=place, found_time=found_time)
                pic = pic[0:-4] + '__' + str(new_found.id) + '__' + pic[-4:]
                new_found.icon = pic

            else:
                new_found = Found(item=item, place=place, found_time=found_time, detail=detail)
                pic = pic[0:-4] + '__' + str(new_found.id) + '__' + pic[-4:]
                new_found.icon = pic

            db.session.add(new_found)
            db.session.commit()

    return redirect(url_for('main.home_stu_found'))


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


# lost and found system -----------------------------------------------------------------------------------------------------------------------------------------------------------------


@student.route('/mark_done_lost')
def mark_done_lost():
    id = request.args.get('id')
    page = request.args.get('page')

    lost = Lost.query.get(id)
    lost.is_done = True
    db.session.add(lost)
    db.session.commit()

    return redirect(url_for('student.lost_and_found_lost', page=page))


@student.route('/mark_done_found')
def mark_done_found():
    id = request.args.get('id')
    page = request.args.get('page')

    found = Found.query.get(id)
    found.is_done = True
    db.session.add(found)
    db.session.commit()

    return redirect(url_for('student.lost_and_found_found', page=page))


@student.route("/home_stu_lost_and_found/lost")
def lost_and_found_lost():
    """
    The function for showing the lost information in the lost and found system
    """
    pagenum = int(request.args.get('page', 1))
    pagination = Lost.query.paginate(page=pagenum, per_page=5)
    return render_template(".html", function="lostAndFound", pagination=pagination, pagenum=pagenum)     # 待核对


@student.route("/home_stu_lost_and_found/found")
def lost_and_found_found():
    """
    The function for showing the found information in the lost and found system
    """
    pagenum = int(request.args.get('page', 1))
    pagination = Found.query.paginate(page=pagenum, per_page=5)
    return render_template(".html", function="lostAndFound", pagination=pagination, pagenum=pagenum)     # 待核对


@student.route("/home_stu_lost_and_found/details")
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

        return render_template(".html", function="lostAndFound", lnf_type=lnf_type, lost=lost,
                               reply_list=reply_list)       # 待核对

    elif lnf_type == 'found':
        found_id = request.args.get('found_id')

        # get the list of replies of this piece of information
        found = Found.query.filter_by(id=found_id).first()
        reply_list = found.replies

        return render_template(".html", function="lostAndFound", lnf_type=lnf_type, found=found,
                               reply_list=reply_list)       # 待核对

    return render_template(".html", function="lostAndFound")      # 待核对


@student.route("/home_stu_change", methods=['GET','POST'])
def stu_change():
    if request.method == "post":
        icon = request.files.get('icon')
        print(icon)
    return render_template('samples/studentIndex.html',function="index")


@student.route("home_stu_lost_and_found/lost", methods=['GET','POST'])
def stu_lost():
    return render_template('samples/studentLost.html',function="lost and found")


@student.route("/home_stu_lost_and_found/lost_detail", methods=['GET','POST'])
def lost_detail():
    return  render_template('samples/lostDetail.html', function="lost and found")
