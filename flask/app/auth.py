from sqlite3 import IntegrityError
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # TODO: Refactor using JSON data
        form = request.form
        username = form.get('username')
        password = form.get('password')
        email = form.get('email')
        error = None

        # TODO: Validate input
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            try: 
                # TODO: Insert complete user data
                db.session.add(User(username=username, email=email, password_hash=generate_password_hash(password)))
                db.session.commit()
            except IntegrityError:
                error = f"User {username} already exists."
            else:
                return redirect(url_for("index"))

        flash(error)

    return render_template('auth/signup.html')

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # TODO: Refactor using JSON data
        form = request.form # data = request.get_json()
        email = form.get('email')
        password = form.get('password')
        error = None
        user = User.query.filter_by(email=email).first()
        
        if user is None or not check_password_hash(user.password_hash, password):
            error = 'Incorrect email or password.'

        if error is None:
            login_user(user)
            return redirect(url_for('index'))
        
        flash(error, 'error')
        
    return render_template('auth/signin.html')

@bp.route('/signout', methods=['GET'])
def signout():
    logout_user()
    return redirect(url_for('index'))

# TODO: Implement view and edit user profile, DO USE decorator @login_required