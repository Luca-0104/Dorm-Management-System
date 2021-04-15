from flask import Blueprint

dormAdmin = Blueprint('dormAdmin', __name__)

from . import views
