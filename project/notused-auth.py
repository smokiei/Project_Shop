# notused-auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash,Response
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from .modelsNew import User
from .modelsNew import Item
from .modelsNew import Img
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('signin.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/create', methods=['POST'])
def create_post():



    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    title = request.form.get('title')
    price = request.form.get('price')
    user = current_user.id  # if this returns a user, then the email already exists in database
    pic = img.id
    print(pic)
    print(user)
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_post = Item(title=title, price=price, id_user=user, id_photo=pic)

    # add the new user to the database
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('main.create'))




@auth.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)

@auth.route('/katalog')
def katalog():
 #   items = Item.query.order_by(Item.price).all()

    sql = text('SELECT t1.*, t2.name FROM Item t1 '
            'LEFT JOIN Img t2 ON t1.id_photo=t2.id ')
    query = db.session.query(Item, Img).from_statement(sql).params()
    items = query.all()

    return render_template('pricing.html', data=items)
