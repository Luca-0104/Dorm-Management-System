@article_bp.route('/all')
def all_article():
    id = request.args.get('id')
    user=User.query.get('id')
    return render_template('article/all1.html',user=user)