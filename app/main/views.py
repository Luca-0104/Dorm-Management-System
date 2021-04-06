from flask import request, redirect, render_template, url_for

from app.main import main
from app.auth.views import get_role_true


@main.route('/', methods=['GET', 'POST'])
def index():
    get_role_true()     # if we are in the index page, we should get ready for getting the role_id
    return render_template("samples/myindex.html")
