@dormAdmin.route('/delete', endpoint='delete')
def delete():
    id = request.args.get('id')
    user = User.query.get(id)
    user.is_deleted = False
    db.session.commit()
    return redirect(url_for('dormAdmin.home'))
