from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from .auth import get_perth_suburbs
from .enums import ResponseMessage, ResponseStatus
from .tools import json_response

bp = Blueprint('profile', __name__, url_prefix='/profile')

@login_required
@bp.route('/', methods=['GET'])
def profile_view():
    return render_template('profile/view_profile.html', user=current_user)

@login_required
@bp.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.get(current_user.id)

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'suburb' in data:
            user.suburb = data['suburb']

        db.session.commit()
        return json_response(ResponseStatus.SUCCESS, ResponseMessage.PROFILE_UPDATED_SUCCESS, {'success': True}), 200

    elif request.method == 'GET':
        suburbs = get_perth_suburbs()
        return render_template('profile/edit_profile.html', user=current_user, suburbs=suburbs)

@login_required
@bp.route('/password', methods=['POST'])
def change_password():
    data = request.get_json()
    current_password = data['currentPassword']
    new_password = data['newPassword']

    user = User.query.get(current_user.id)

    if not check_password_hash(user.password_hash, current_password):
        return json_response(ResponseStatus.ERROR, ResponseMessage.INCORRECT_CURRENT_PASSWORD, {'success': False}), 401

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return json_response(ResponseStatus.SUCCESS, ResponseMessage.PASSWORD_CHANGED_SUCCESS, {'success': True}), 200

@login_required
@bp.route('/update_image', methods=['POST'])
def update_image():
    data = request.get_json()
    imageUrl = data.get('imageUrl')
    print("Received imageUrl:", imageUrl)
    if imageUrl:
        current_user.profile_image = imageUrl.split('/')[-1]
        db.session.commit()
        return json_response(ResponseStatus.SUCCESS, "Profile image updated successfully.")
    return json_response(ResponseStatus.ERROR, "Failed to update image.")