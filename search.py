from flask import Flask, render_template, request, redirect
import fileutils


@app.route('/list/')
def student_list():
    student_list = fileutils.file_read().items()
    print('student_list:%s' % student_list)
    return render_template('list.html', student_list=student_list)

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
