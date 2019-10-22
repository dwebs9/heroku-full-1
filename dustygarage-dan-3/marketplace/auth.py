from flask import (
    Blueprint, flash, render_template, request, url_for, redirect, Markup, session
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


# create a blueprint
bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if(form.validate_on_submit()):
        emailid = form.emailid.data
        password = form.password.data
        u1 = User.query.filter_by(emailid=emailid).first()

        next_page = request.args.get('next')
        print('#################')

        print(next_page)
        print('#################')

        # if there is no user with matching username or password is incorrect
        if u1 is None or not check_password_hash(u1.password_hash, password):
            flash(u'Incorrect Login Credentials', 'alert alert-danger')
            return redirect(url_for('auth.login'))
        login_user(u1)
        viewed = []
        session['vieweditems'] = viewed
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
            print('#################')

        print(next_page)
        print('#################')

        return redirect(next_page)
    return render_template('user.html', form=form, heading='Login')


@bp.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    register_error = None
    if form.validate_on_submit():
        print('Registration form Submitted')
        # retrieve Username, Pwd & Email
        name = form.name.data
        lastName = form.lastName.data
        pwd = form.password.data
        email = form.email.data
        pwd_hash = generate_password_hash(pwd)

        # query db to check if there are any existing users already registered with that username
        user_exists = User.query.filter_by(emailid=email).first()

        if user_exists:
            register_error = "The Email \"{}\" is already registered, please try another email or <a href=\"/login\" class=\"alert-link\">Login here</a>" .format(
                email)
            flash((Markup(register_error)), 'alert alert-danger')
            return redirect(url_for('auth.register'))

        # create a new db user

        new_user = User(name=name, lastName=lastName,
                        password_hash=pwd_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        print('COMMITED TO DB')
        register_success = "The Email \"{}\"successfully registered" .format(
            email)
        flash((Markup(register_success)), 'alert alert-info')
        # redirect

        return redirect(url_for('auth.login'))

    return render_template('user.html', form=form, heading='Register')
