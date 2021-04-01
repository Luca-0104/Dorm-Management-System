from flask import Blueprint

from ..models import Permission

main = Blueprint('main', __name__)

from . import views, errors        # to avoid endless recursive import, this statement should be after the defining of main


# 把Permission类加入到模板上下文，以保证Permission类的所有常量都能在模板中访问，而避免每次调用render_template()的时候都多添加一个模板参数
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)