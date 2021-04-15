@dormAdmin.route('/delete', endpoint='delete')
def delete():
    id = request.args.get('id')
    student = User.query.get(id)
    student.is_deleted = True
    db.session.commit()
    return redirect(url_for('dormAdmin.home'))
