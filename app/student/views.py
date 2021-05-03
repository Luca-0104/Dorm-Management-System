from flask import request, render_template
from flask import Blueprint
from .. import db
from app.models import Message, Student

message_bp = Blueprint('message', __name__)

@message_bp.route('/add', method=['GET', 'POST'])
def add_message():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        uid = request.form.get('uid')
        message = Message()
        message.title = title
        message.content = content
        message.stu_id = uid
        db.session.add(message)
        db.session.commit()
        return 'submit successfully！'
    else:
        students = Student.query.filter(Student.is_deleted == False).all()
        return render_template('message/add_message.html', students=students)




