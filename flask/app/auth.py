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
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
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
                db.session.add(User(username=username, password=generate_password_hash(password)))
                db.session.commit()
            except IntegrityError:
                error = f"User {username} already exists."
            else:
                # TODO: Redirect to dashboard page
                return redirect(url_for("auth.signin"))

        flash(error)

    return render_template('auth/signup.html')

@bp.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            error = 'Incorrect username or password.'

        if error is None:
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash(error)
        
    return render_template('auth/signin.html')

@bp.route('/signout', methods=['POST'])
def sign_out():
    logout_user()
    return redirect(url_for('index'))

# TODO: Implement view and edit user profile, DO USE decorator @login_required