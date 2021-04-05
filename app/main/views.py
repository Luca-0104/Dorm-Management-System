from flask import request, redirect, render_template, url_for

from app.main import main


@main.route('/', methods=['GET', 'POST'])
def index():
    global role_id
    if request.method == 'POST':
        role_id = request.args.get('identification')
        return redirect(url_for('main.login'))  

    return render_template("samples/myindex.html")
