from flask_app import app # import app to run routes
from flask_app.models import user, post
from flask import render_template, redirect, session, request, flash
@app.route('/wall')
def load_wall():
    if 'user_id' not in session:
        return redirect('/')
    wall_data = post.Post.get_all_post_data(session['user_id']) # get all posts, comments, and people involved
    if not wall_data['user']: # if the user has not made any posts or comments, they have no instance of the User class yet.
        wall_data['user'] = user.User.get_user_by_id({'id': session['user_id']})
    return render_template('user_wall.html', user_data = wall_data['user'], all_posts = wall_data['posts'])
@app.route('/post/publish', methods=['POST'])
def publish_post():
    if not post.Post.validate_post(request.form):
        return redirect('/wall')
    post_data = {
        'post': request.form['post'],
        'user_id': session['user_id']
    }
    new_post = post.Post.save_post(post_data)
    return redirect('/wall')
@app.route('/post/delete/<int:post_id>')
def delete_post(post_id):
    post.Post.delete_post({'id': post_id})
    return redirect('/wall')
    pass