from sqlite3 import IntegrityError
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User
from .enums import Topic

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
                new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                error = f"User {username} already exists."
            else:
                # Login user after successful registration
                login_user(new_user)
                return redirect(url_for("auth.topic_select"))

        flash(error)

    return render_template('auth/signup.html')

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username') 
        password = data.get('password')
        user = User.query.filter_by(username=username).first() 
        
        if user is None or not check_password_hash(user.password_hash, password):
            return jsonify({'success': False, 'message': 'Incorrect username or password.'}), 401

        login_user(user)
        return jsonify({'success': True, 'redirect': url_for('index')})

    return render_template('auth/signin.html')

@bp.route('/signout', methods=['GET'])
def signout():
    logout_user()
    return redirect(url_for('index'))

@bp.route('/topic-select', methods=['GET', 'POST'])
@login_required
def topic_select():
    if request.method == 'POST':
        selected_topics = request.form.getlist('topics')
        if 2 <= len(selected_topics) <= 6:
            current_user.interested_topics = ','.join(selected_topics)
            db.session.commit()
            return redirect(url_for('index.index'))
        else:
            flash('Please select at least 2 topics, but no more than 6.')

    topics = [topic.value for topic in Topic]
    return render_template('auth/topic_select.html', topics=topics)

# TODO: Implement view and edit user profile, DO USE decorator @login_required