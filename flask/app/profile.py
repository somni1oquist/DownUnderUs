import errno
import os
from flask import Blueprint, current_app, jsonify, render_template, request
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from .auth import get_perth_suburbs
from .enums import ResponseMessage, ResponseStatus
from .tools import json_response
from werkzeug.exceptions import NotFound

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
    if imageUrl:
        current_user.profile_image = imageUrl.split('/')[-1]
        db.session.commit()
        return json_response(ResponseStatus.SUCCESS, "Profile image updated successfully.")
    return json_response(ResponseStatus.ERROR, "Failed to update image.")

@login_required
@bp.route('/delete_image', methods=['DELETE'])
def delete_image():
    if current_user.profile_image:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_image)
        try:
            if os.path.exists(file_path):  
                os.remove(file_path)
        except OSError as e:
            if e.errno != errno.ENOENT: 
                raise NotFound("The file could not be found.")
        current_user.profile_image = None
        db.session.commit()
        return json_response(ResponseStatus.SUCCESS, "Profile image deleted successfully.")
    
    return json_response(ResponseStatus.ERROR, "No profile image to delete.")