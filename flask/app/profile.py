from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from .auth import get_perth_suburbs

bp = Blueprint('profile', __name__, url_prefix='/profile')

@login_required
@bp.route('/', methods=['GET'])
def profile_view():
    return render_template('profile/view_profile.html', user=current_user)

@login_required
@bp.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    suburbs = get_perth_suburbs()

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
        return jsonify({'success': True, 'message': 'Profile updated successfully!'}), 200

    elif request.method == 'GET':
        return render_template('profile/edit_profile.html', user=current_user, suburbs=suburbs)

@login_required
@bp.route('/password', methods=['POST'])
def change_password():
    data = request.get_json()
    current_password = data['currentPassword']
    new_password = data['newPassword']

    user = User.query.get(current_user.id)

    if not check_password_hash(user.password_hash, current_password):
        return jsonify({'success': False, 'message': 'Incorrect current password.'}), 401

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Password changed successfully!'}), 200