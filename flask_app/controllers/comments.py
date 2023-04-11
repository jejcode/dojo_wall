from flask_app import app # import app to run routes
from flask_app.models import user, post, comment # import models to talk to db
from flask import render_template, redirect, session, request, flash # flask modules to make routes work right

@app.route('/comment/add', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return redirect('/')
    if not comment.Comment.validate_comment(request.form):
        return redirect('/wall')
    data = {
        'comment': request.form['comment'],
        'post_id': request.form['post_id'],
        'user_id': session['user_id']
    }
    new_comment_id = comment.Comment.save(data)
    print(new_comment_id)
    # don't render a POST request
    return redirect('/wall')