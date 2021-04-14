from flask import Blueprint

auth = Blueprint('dormAdmin', __name__)

from . import views
