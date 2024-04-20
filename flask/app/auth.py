from sqlite3 import IntegrityError
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User
from .enums import ResponseMessage, ResponseStatus, Topic
from .tools import json_response

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    suburbs = get_perth_suburbs()
    if request.method == 'POST':
        data = request.json if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        suburb = data.get('suburb')
        
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'success': False, 'message': f"An account with email {email} already exists."}), 409

        try:
            new_user = User(email=email, username=username,
                            password_hash=generate_password_hash(password),
                            suburb=suburb)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return jsonify({'success': True, 'message': 'Registration successful.', 'redirect': url_for("index.index")})
        except IntegrityError:
            db.session.rollback()
            return jsonify({'success': False, 'message': f"Account with email {email} cannot be created."}), 500

    return render_template('auth/signup.html', suburbs=suburbs)

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
        # TODO: Rewrite this to use JSON response
        return jsonify({'success': True, 'redirect': url_for('index.index')})

    return render_template('auth/signin.html')

@bp.route('/signout', methods=['GET'])
def signout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/topic-select', methods=['GET', 'POST'])
@login_required
def topic_select():
    if request.method == 'POST':
        selected_topics = request.get_json().get('topics')
        # Validate selected topics
        if len(selected_topics) < 2 or len(selected_topics) > 6:
            return json_response(ResponseStatus.ERROR, ResponseMessage.TOPIC_RANGE), 400
        
        current_user.interested_topics = ','.join(selected_topics)
        db.session.commit()
        return json_response(ResponseStatus.SUCCESS, ResponseMessage.TOPIC_SELECTED,\
                            {'redirect': url_for('index.index')}), 200

    topics = [topic.value for topic in Topic]
    return render_template('auth/topic-select.html', topics=topics)

def get_perth_suburbs():
    # List of suburbs in Perth, WA
    suburbs = [
        "Perth", "Armadale", "Bayswater", "Canning", "Cockburn", "Fremantle",
        "Gosnells", "Joondalup", "Kalamunda", "Kwinana", "Melville"
    ]
    return suburbs


def get_perth_suburbs():
    # List of suburbs in Perth, WA
    suburbs = [
        "Perth", "Armadale", "Bayswater", "Canning", "Cockburn", "Fremantle",
        "Gosnells", "Joondalup", "Kalamunda", "Kwinana", "Melville"
    ]
    return suburbs


# TODO: Implement view and edit user profile, DO USE decorator @login_required