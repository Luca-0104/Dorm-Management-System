from flask import Flask, render_template, request, redirect


@app.route('/login/', methods=["POST", "GET"])
def login():

    if request.method == 'GET':
        username = request.stu.get('username')
        password = request.stu.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    print('username:%s,password:%s' % (username, password))

    if username and password:
        if username == "admin" and password == "admin":
            return redirect('/list')
        else:
            print('username or password is wrong')
    else:
        print('need username and password')

    return render_template('login.html')
