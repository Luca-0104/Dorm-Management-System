from flask import Blueprint

sysAdmin = Blueprint('sysAdmin', __name__)

from . import views
