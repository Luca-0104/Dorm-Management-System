# from datetime import datetime
#
# from flask import request, redirect, render_template, url_for, flash
# from flask_login import UserMixin, current_user
# from flask_wtf import FlaskForm
# from wtforms import TextAreaField, SubmitField
# from wtforms.validators import DataRequired, Length
#
# from .. import db, student
# from app.main.forms import MessageForm
# from app.models import Message
#
#
# # 新增数据库模型
# class Message(db.Model):
#     __tablename__ = 'messages'
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('stu_id'))
#     recipient_id = db.Column(db.Integer, db.ForeignKey('dorm_id'))
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Message {}>'.format(self.body)
#
#
# # user 模型
# class User(UserMixin, db.Model):
#     messages_sent = db.relationship('Message',
#                                     foreign_keys='Message.sender_id',
#                                     backref='sender', lazy='dynamic')
#     messages_received = db.relationship('Message',
#                                         foreign_keys='Message.recipient_id',
#                                         backref='recipient', lazy='dynamic')
#
#
# # 私信表单
#
# class MessageForm(FlaskForm):
#     message = TextAreaField('Message', validators=[
#         DataRequired(), Length(min=0, max=140)])
#     submit = SubmitField('Submit')
#
#
# # 私信的视图函数
# @student.route('/send_message/<recipient>', methods=['GET', 'POST'])
# def send_message(recipient):
#     user = User.query.filter_by(username=recipient).first_or_404()
#     form = MessageForm()
#     if form.validate_on_submit():
#         msg = Message(author=current_user, recipient=user,
#                       body=form.message.data)
#         db.session.add(msg)
#         db.session.commit()
#         flash('Your message has been sent.')
#         return redirect(url_for('main.user', username=recipient))
#     return render_template('send_message.html', title='Send Message',
#                            form=form, recipient=recipient)



from flask import request, render_template, redirect, url_for
from flask_login import current_user

from . import student
from .. import db
from ..models import Student, Repair


# @student.route('', methods=['GET', 'POST'])
# def reply():
#     """
#     The function for replying the message
#     """
#     if request.method == 'POST':


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
    pagenum = int(request.args.get('page', 1))
    repair_list = Repair.query.filter_by(stu_id=stu_id).paginate(page=pagenum, per_page=5)
    return render_template("samples/messageRepair.html", function="message", pagination=repair_list)



