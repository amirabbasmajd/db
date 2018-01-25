import datetime

from flask import (
    render_template,
    url_for,
    redirect,
    request,
    flash
)
from flask_login import login_user, logout_user
from pymongo.errors import DuplicateKeyError

from app import mongo, login_manager
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.email import send_email
from app.user import User


@login_manager.user_loader
def load_user(username):
    u = mongo.db.users.find_one({'_id': username})
    if not u:
        return None
    return User(u['_id'])


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html', title='Log In', form=LoginForm())

    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'_id': username})
        if user and User.verify_password(user['password'], password):
            user_obj = User(user['_id'])
            login_user(user_obj)
            return redirect(request.args.get("next") or url_for("main.home"))
        flash("Wrong username or password.", category='error')
    return render_template('auth/login.html', title='Log In', form=form)


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('auth/registration.html', title='Registration',
                               form=RegistrationForm())

    form = RegistrationForm()
    username = form.username.data
    full_name = form.full_name.data
    email = form.email.data
    password = form.password.data

    if form.validate_on_submit():
        try:
            mongo.db.users.insert({'_id': username,
                                   'full_name': full_name,
                                   'email': email,
                                   'password': User.generate_hash(password),
                                   'registered_in': datetime.datetime.utcnow()
                                   })

            flash('Successfully created an account!', category='success')
            # send_email(email, full_name, username, password)
            return redirect(url_for("auth.login"))
        except DuplicateKeyError:
            flash('Username already exist', category='error')
    return render_template('auth/registration.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You just signed out', category='warning')
    return redirect(url_for('auth.login'))
