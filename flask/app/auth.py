from sqlite3 import IntegrityError
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User
from .enums import ResponseMessage, ResponseStatus, Topic
from .tools import json_response, update_user_points


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        suburb = data.get('suburb')

        if not username:
            return json_response(ResponseStatus.ERROR, ResponseMessage.USERNAME_REQUIRED, {'success': False}), 400
        if not email:
            return json_response(ResponseStatus.ERROR, ResponseMessage.EMAIL_REQUIRED, {'success': False}), 400
        if not password:
            return json_response(ResponseStatus.ERROR, ResponseMessage.PASSWORD_REQUIRED, {'success': False}), 400
        if not suburb:
            return json_response(ResponseStatus.ERROR, ResponseMessage.SUBURB_REQUIRED, {'success': False}), 400
        if User.query.filter_by(email=email).first() is not None:
            return json_response(ResponseStatus.ERROR, ResponseMessage.EMAIL_EXISTS, {'success': False}), 409

        try:
            new_user = User(email=email, username=username,
                            password_hash=generate_password_hash(password),
                            suburb=suburb)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            
            return json_response(ResponseStatus.SUCCESS, ResponseMessage.REGISTRATION_SUCCESSFUL, {'success': True, 'redirect': url_for("index.index")}), 201
        except IntegrityError:
            db.session.rollback()
            return json_response(ResponseStatus.ERROR, ResponseMessage.ACCOUNT_CREATION_FAILED, {'success': False}), 500
    suburbs = get_perth_suburbs()
    return render_template('auth/signup.html', suburbs=suburbs)

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        redirect_url = data.get('callbackUrl') or url_for('index.index')

        if not email:
            return json_response(ResponseStatus.ERROR, ResponseMessage.EMAIL_REQUIRED, {'success': False}), 400
        if not password:
            return json_response(ResponseStatus.ERROR, ResponseMessage.PASSWORD_REQUIRED, {'success': False}), 400
        
        user = User.query.filter_by(email=email).first() 
        if user is None or not check_password_hash(user.password_hash, password):
            return json_response(ResponseStatus.ERROR, ResponseMessage.INCORRECT_CREDENTIALS, {'success': False}), 401

        login_user(user)
        update_user_points(user.id,5)
        return json_response(ResponseStatus.SUCCESS, ResponseMessage.LOGIN_SUCCESS,{'success': True, 'redirect': redirect_url, 'points_added': 5}), 200

    return render_template('auth/signin.html')

@bp.route('/signout', methods=['GET'])
def signout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/topic-select', methods=['POST'])
@login_required
def topic_select():
    data = request.get_json()
    selected_topics = data.get('topics')
    redirect_url = data.get('callbackUrl') or url_for('index.index')
    # Validate selected topics
    if len(selected_topics) < 2 or len(selected_topics) > 6:
        return json_response(ResponseStatus.ERROR, ResponseMessage.TOPIC_RANGE), 400
    
    current_user.interested_topics = ','.join(selected_topics)
    db.session.commit()
    return json_response(ResponseStatus.SUCCESS, ResponseMessage.TOPIC_SELECTED,\
                        {'redirect': redirect_url}), 200

def get_perth_suburbs():
    # List of suburbs in Perth, WA
    suburbs = [
        "Perth", "Armadale", "Bayswater", "Canning", "Cockburn", "Fremantle",
        "Gosnells", "Joondalup", "Kalamunda", "Kwinana", "Melville"
    ]
    return suburbs