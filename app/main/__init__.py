from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors        # to avoid endless recursive import, this statement should be after the defining of main


