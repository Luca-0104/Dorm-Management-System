from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    """
    a method for loading the user
    flask-login 要求的一个函数，在扩展需要从数据库获取指定标识符的user时调用
    :param user_id: The id of the user
    :return: An object of User or None
    """
    return User.query.get(int(user_id))


# 权限常量（2^n, 所以组合求和不会冲突）
class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


# 定义Role模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')             # 在数据库模型中定义关系
    # default = db.Column(db.Boolean, default=False, index=True)  # 是否为默认角色（只能有一种是默认角色）
    permissions = db.Column(db.Integer)                         # 权限码的和

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0              # permissions字段默认被sqlalchemy设置成None，我们需要初始化其为0

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
            'Student': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Dormitory_administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'System_administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'Student'                                       # 设置默认用户为普通User
        for r in roles:                                                # 遍历整个字典
            role = Role.query.filter_by(name=r).first()
            if role is None:                                        # 如果还没有这个角色就创建一个
                role = Role(name=r)
            for perm in roles[r]:                                   # 遍历对应角色的权限列表
                role.add_permission(perm)                           # 给角色添加对应范围内的权限
            role.default = (role.name == default_role)              # 如果是默认角色，则将default设置为True
            db.session.add(role)
        db.session.commit()


# 定义User模型
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.String(64), unique=True, index=True)
    stu_wor_id = db.Column(db.String(64), unique=True, index=True)
    user_name = db.Column(db.String(64), unique=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 在数据库模型中定义关系
    password_hash = db.Column(db.String(128))
    # 资料页面信息
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)


    def __repr__(self):
        return '<User %r>' % self.user_name

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
        return self.can(Permission.ADMIN)

    # 刷新用户的最后访问时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
