from flask import request, redirect, render_template, url_for

from app.main import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("samples/myindex.html")
