from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from .tableInfo import stu_list, gue_list, da_list, user_list


@login_manager.user_loader
def load_user(user_id):
    """
    a method for loading the user
    flask-login 要求的一个函数，在扩展需要从数据库获取指定标识符的user时调用
    :param user_id: The id of the user
    :return: An object of User or None
    """
    return User.query.get(int(user_id))


class Tools:
    """
    All the tool methods for creating the tables
    """

    @staticmethod
    def update_db():
        db.drop_all()
        db.create_all()
        Tools.fill_all_tables()

    @staticmethod
    def fill_all_tables():
        """
        Fill all the tables in an specific order.
        This should be used in the console only a single time.
        """
        Role.insert_roles()
        DormBuilding.insert_dorm_buildings()
        Student.insert_students()
        Guest.insert_guests()
        DAdmin.insert_das()
        User.insert_users()


# 权限常量（2^n, 所以组合求和不会冲突）
class Permission:
    ACCUSE = 1
    PAYMENT = 2
    LOST_ANNOUNCE = 4
    DORM_ADMIN = 8
    SYS_ADMIN = 16


# ------------------------------------------------ message tables ---------------------------------------------------


class Repair(db.Model):
    __tablename__ = 'repairs'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), nullable=False)
    detail = db.Column(db.Text)
    date = db.Column(db.Date(), default=datetime.utcnow)
    finish_time = db.Column(db.DateTime(), unique=False)
    is_repaired = db.Column(db.Boolean, default=False)
    stu_id = db.Column(db.Integer, db.ForeignKey('students.id'), unique=False)  # define the relation with Student
    replies = db.relationship('ReplyRepair', backref='repair')

    def __repr__(self):
        return '<Repair %r>' % self.item


class Complain(db.Model):
    __tablename__ = 'complains'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.Text)
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    stu_id = db.Column(db.Integer, db.ForeignKey('students.id'), unique=False)
    replies = db.relationship('ReplyComplain', backref='complain')

    def __repr__(self):
        return '<Complain %r>' % self.detail


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.Text)
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    da_id = db.Column(db.Integer, db.ForeignKey('dormAdmins.id'), unique=False)

    def __repr__(self):
        return '<Notification %r>' % self.detail


# ------------------------------------------------ lost & found tables ---------------------------------------------------


class Lost(db.Model):
    __tablename__ = 'lost_items'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    place = db.Column(db.String(64), default='unknown')
    lost_time = db.Column(db.DateTime(), default=datetime.utcnow)
    icon = db.Column(db.String(256), default='upload/lost/default__0__.jpg')
    detail = db.Column(db.Text, default='nothing')
    stu_id = db.Column(db.Integer, db.ForeignKey('students.id'), unique=False)
    post_time = db.Column(db.DateTime(), default=datetime.utcnow)
    replies = db.relationship('ReplyLost', backref='lost')
    is_done = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Lost %r>' % self.item


class Found(db.Model):
    __tablename__ = 'found_items'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), nullable=False)
    place = db.Column(db.String(64), nullable=False)
    found_time = db.Column(db.DateTime(), nullable=False)
    icon = db.Column(db.String(256), default='upload/found/default__0__.jpg')
    detail = db.Column(db.Text, default='nothing')
    stu_id = db.Column(db.Integer, db.ForeignKey('students.id'), unique=False)
    post_time = db.Column(db.DateTime(), default=datetime.utcnow)
    replies = db.relationship('ReplyFound', backref='found')
    is_done = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Found %r>' % self.item


# ------------------------------------------------ reply tables ---------------------------------------------------


# a table for all the replies of repair message
class ReplyRepair(db.Model):
    __tablename__ = 'repair_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    repair_id = db.Column(db.Integer, db.ForeignKey('repairs.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# a table for all the replies of complain message
class ReplyComplain(db.Model):
    __tablename__ = 'complain_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    complain_id = db.Column(db.Integer, db.ForeignKey('complains.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class ReplyLost(db.Model):
    __tablename__ = 'lost_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    lost_id = db.Column(db.Integer, db.ForeignKey('lost_items.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    replies = db.relationship('ReplyReplyLost', backref='lost_reply')


class ReplyReplyLost(db.Model):
    """
    A table of nested replies of lost_reply
    """
    __tablename__ = 'lost_reply_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    lost_reply_id = db.Column(db.Integer, db.ForeignKey('lost_replies.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class ReplyFound(db.Model):
    __tablename__ = 'found_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    found_id = db.Column(db.Integer, db.ForeignKey('found_items.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    replies = db.relationship('ReplyReplyFound', backref='found_reply')


class ReplyReplyFound(db.Model):
    """
    a table of nested replies of found_reply
    """
    __tablename__ = 'found_reply_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    found_reply_id = db.Column(db.Integer, db.ForeignKey('found_replies.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# -------------------------------------------------------------------------------------------------------------------------------


# The table of dormitory buildings
class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    gue_name = db.Column(db.String(64), unique=False, nullable=False)
    phone = db.Column(db.String(64), unique=False, nullable=False)
    stu_id = db.Column(db.Integer, db.ForeignKey('students.id'), unique=False)  # define the relation with Student
    note = db.Column(db.String(64), unique=False, default='Nothing')
    arrive_time = db.Column(db.DateTime(), default=datetime.utcnow)
    leave_time = db.Column(db.DateTime(), unique=False)
    is_deleted = db.Column(db.Boolean, default=False)
    has_left = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Guest %r>' % self.gue_name

    @staticmethod
    def insert_guests():
        """
        This is a method for inserting the guests information, which means fulling the Guest table.
        This should be used in the console only a single time.
        """
        for gue_info in gue_list:
            gue_name = gue_info[0]
            phone = gue_info[1]
            stu_id = gue_info[2]

            new_gue = Guest(gue_name=gue_name, phone=phone, stu_id=stu_id)

            db.session.add(new_gue)
            db.session.commit()


# The table of dormitory buildings
class DormBuilding(db.Model):
    __tablename__ = 'dorm_buildings'
    id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(64), unique=True)
    students = db.relationship('Student', backref='building')
    dormAdmins = db.relationship('DAdmin', backref='building')

    def __repr__(self):
        return '<DormBuilding %r>' % self.building_name

    # 添加静态方法，用于自动在数据库中创建并添加宿舍楼(请在shell中使用此函数！！！)
    @staticmethod
    def insert_dorm_buildings():
        buildings = [
            'DormBuilding_1',
            'DormBuilding_2',
            'DormBuilding_3',
            'DormBuilding_4',
            'DormBuilding_5',
            'DormBuilding_6',
            'DormBuilding_7',
            'DormBuilding_8',
            'DormBuilding_9',
            'DormBuilding_10',
            'DormBuilding_11',
            'DormBuilding_12',
            'DormBuilding_13',
        ]
        for b in buildings:  # 遍历整个字典
            building = DormBuilding.query.filter_by(building_name=b).first()
            if building is None:  # 如果还没有这个楼就创建一个
                building = DormBuilding(building_name=b)
            db.session.add(building)
        db.session.commit()


# The table of dormitory administrator information
class DAdmin(db.Model):
    __tablename__ = 'dormAdmins'
    id = db.Column(db.Integer, primary_key=True)
    da_name = db.Column(db.String(64), nullable=False)
    da_number = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True)
    building_id = db.Column(db.Integer, db.ForeignKey('dorm_buildings.id'), unique=False, nullable=False)
    enroll_date = db.Column(db.DateTime(), default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    is_registered = db.Column(db.Boolean, default=False)

    # relationship with some types of messages
    notifications = db.relationship('Notification', backref='dormAdmin')  # define the relation with the Notification table


    def __repr__(self):
        return '<DAdmin %r>' % self.da_name

    def delete_da(self):
        """
        The function for delete dormitory administrator logically
        """
        self.is_deleted = True
        db.session.add(self)
        db.session.commit()

    def register_da(self):
        """
        The function for register dormitory administrator logically
        (Use this function if the dormitory administrator registers as an user)
        """
        self.is_registered = True
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def insert_das():
        """
        This is a method for inserting the dormitory administrator information, which means fulling the dormitory administrator table.
        This should be used in the console only a single time.
        """
        for da_info in da_list:
            da_name = da_info[0]
            da_number = da_info[1]
            phone = da_info[2]
            email = da_info[3]
            building_id = da_info[4]

            new_da = DAdmin(da_name=da_name, da_number=da_number, phone=phone, email=email, building_id=building_id)
            db.session.add(new_da)
            db.session.commit()


# The table of dormitory information
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    stu_name = db.Column(db.String(64), unique=False, nullable=False)
    stu_number = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True)
    college = db.Column(db.String(64), unique=False, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('dorm_buildings.id'), unique=False, nullable=False)
    room_number = db.Column(db.Integer, unique=False, nullable=False)
    enroll_date = db.Column(db.DateTime(), default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    is_registered = db.Column(db.Boolean, default=False)
    guests = db.relationship('Guest', backref='student')  # define the relation with the Guest table

    # relationship with some kinds of messages
    repairs = db.relationship('Repair', backref='student')  # define the relation with the Repair table
    complains = db.relationship('Complain', backref='student')  # define the relation with the Complain table

    # relationship with the 'lost and found' system
    lost_items = db.relationship('Lost', backref='student')    # define the relation with the Lost table
    found_items = db.relationship('Found', backref='student')    # define the relation with the Found table

    def __repr__(self):
        return '<Student %r>' % self.stu_name

    def delete_stu(self):
        """
        The function for delete student logically
        """
        self.is_deleted = True
        db.session.add(self)
        db.session.commit()

    def register_stu(self):
        """
        The function for register student logically
        (Use this function if the student registers as an user)
        """
        self.is_registered = True
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def insert_students():
        """
        This is a method for inserting the dorm information, which means fulling the Student table.
        This should be used in the console only a single time.
        """
        for stu_info in stu_list:
            stu_name = stu_info[0]
            stu_number = stu_info[1]
            phone = stu_info[2]
            email = stu_info[3]
            college = stu_info[4]
            building_id = stu_info[5]
            room_number = stu_info[6]

            new_stu = Student(stu_name=stu_name, stu_number=stu_number, phone=phone, email=email, college=college,
                              building_id=building_id, room_number=room_number)
            db.session.add(new_stu)
            db.session.commit()


# The table of different roles (3 roles) of users
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')  # 在数据库模型中定义关系
    permissions = db.Column(db.Integer)  # 权限码的和

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0  # permissions字段默认被sqlalchemy设置成None，我们需要初始化其为0

    def __repr__(self):
        return '<Role %r>' % self.name

    # 添加管理权限的方法
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm  # 位运算符，查看当前权限组合中是否包含指定的权限

    # 添加静态方法，用于自动在数据库中创建并添加角色(请在shell中使用此函数！！！)
    @staticmethod
    def insert_roles():
        roles = {  # 创建一个角色字典，每个value都是对应角色的所有权限列表
            'Student': [Permission.ACCUSE, Permission.PAYMENT, Permission.LOST_ANNOUNCE],
            'Dormitory_administrator': [Permission.DORM_ADMIN, Permission.LOST_ANNOUNCE],
            'System_administrator': [Permission.SYS_ADMIN, Permission.DORM_ADMIN]
        }
        default_role = 'Student'  # 设置默认用户为普通User
        for r in roles:  # 遍历整个字典
            role = Role.query.filter_by(name=r).first()
            if role is None:  # 如果还没有这个角色就创建一个
                role = Role(name=r)
            for perm in roles[r]:  # 遍历对应角色的权限列表
                role.add_permission(perm)  # 给角色添加对应范围内的权限
            role.default = (role.name == default_role)  # 如果是默认角色，则将default设置为True
            db.session.add(role)
        db.session.commit()


# The table of users
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.String(64), unique=True, index=True)
    stu_wor_id = db.Column(db.String(64), unique=True, index=True)
    user_name = db.Column(db.String(64), unique=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 在数据库模型中定义关系
    password_hash = db.Column(db.String(128))
    icon = db.Column(db.String(256), default='upload/avatar/default__0__.jpg')    # The avatar

    # about profiles
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # about replies
    repair_replies = db.relationship('ReplyRepair', backref='user')
    complain_replies = db.relationship('ReplyComplain', backref='user')
    lost_replies = db.relationship('ReplyLost', backref='user')
    found_replies = db.relationship('ReplyFound', backref='user')
    lost_reply_replies = db.relationship('ReplyReplyLost', backref='user')
    found_reply_replies = db.relationship('ReplyReplyFound', backref='user')


    def __repr__(self):
        return '<User %r>' % self.user_name

    @staticmethod
    def insert_users():
        """
        This is a method for inserting the testing user information, which means fulling the User table.
        This should be used in the console only a single time.
        """
        for user_info in user_list:
            email = user_info[0]
            phone = user_info[1]
            stu_wor_id = user_info[2]
            user_name = user_info[3]
            role_id = user_info[4]
            password = user_info[5]

            new_user = User(user_name=user_name, stu_wor_id=stu_wor_id, role_id=role_id, password=password,
                            email=email, phone=phone)

            db.session.add(new_user)
            db.session.commit()

    # 添加密码散列功能
    @property
    def password(self):
        raise AttributeError('pass word is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 添加用于检查用户是否有指定权限的方法
    def can(self, perm):  # 判断用户是否具有某项权限
        return self.role is not None and self.role.has_permission(perm)

    def is_system_administrator(self):  # 判断该用户是否是管理员
        return self.can(Permission.SYS_ADMIN)

    # 刷新用户的最后访问时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
