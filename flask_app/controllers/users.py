from flask_app import app # import app to run instance
from flask import render_template, redirect, session, request, flash # flask modules for routes to work
from flask_app.models import user,post # import models
from flask_bcrypt import Bcrypt # import bcrypt to hash and encrypt passwords
bcrypt = Bcrypt(app) # create an object called bcrypt using app as the argument

@app.route('/') # default route to load index page
def load_login():
    if 'user_id' not in session:
        return render_template('index.html')
    return redirect('/wall')
@app.route('/register', methods=['POST'])
def register_user():
    if not user.User.validate_registration(request.form): # validate user input to match required criteria
        session['form_in_progress'] = request.form # save progress so user can start where they left off if there are errors
        return redirect('/')
    if 'form_in_progress' in session:
        session.pop('form_in_progress')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # create a password hash
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password' : pw_hash # store password hash rather than the actual password
    }
    session['user_id'] = user.User.add_user(data) # set user id to what is returned from query
    return redirect('/wall')
@app.route('/login', methods=['POST'])
def login():

    user_in_db = user.User.get_user_by_email({'email': request.form['email']})
    if not user_in_db:
        flash('Invalid email/password', 'login')
        return redirect('/')
    # compare hash of entered password to hash saved in database
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid email/password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/wall')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')