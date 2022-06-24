import datetime

from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from flask_jwt_extended import create_access_token
from flask_login import login_user, logout_user, login_required
from sqlalchemy import or_

from project import db
from project.mod_auth.forms import SignUpForm, LoginForm
from project.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
# auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    users_demo = User.query.all()
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():
        name_or_email = or_(User.UserName == login_form.email.data, User.Email == login_form.email.data)
        user = User.query.filter(name_or_email).one_or_none()
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember)
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=user, expires_delta=expires)
            session['debug_access_token'] = access_token
            flash(f'Ласкаво просимо, {user.UserName}!')
            return redirect(url_for('main.profile'))
        flash('Невірний логін або пароль', 'error-message')
    return render_template('auth/signin.html', all_users=users_demo, login_form=login_form)


@auth_blueprint.route('/signout')
@login_required
def signout():
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('auth.signin'))


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm(request.form)
    if signup_form.validate_on_submit():
        existing_user = User.query.filter_by(Email=signup_form.email.data).first()
        if existing_user:
            flash(f'Email {existing_user.Email} вже використовується!')
            return redirect(url_for('auth.signup'))
        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User.from_signup(
            name=signup_form.username.data,
            password=signup_form.password.data,
            email=signup_form.email.data)

        db.session.add(new_user)
        db.session.commit()
        flash(f'Користувача {new_user.Email} зареєстровано')
        return redirect(url_for('auth.signin'))
    return render_template('auth/signup.html', signup_form=signup_form)
