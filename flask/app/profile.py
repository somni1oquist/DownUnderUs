import errno
import os
from flask import Blueprint, current_app, jsonify, render_template, request
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User,Title
from .auth import get_perth_suburbs
from .enums import ResponseMessage, ResponseStatus
from .tools import json_response
from werkzeug.exceptions import NotFound
from datetime import datetime, timedelta
from sqlalchemy import or_,func

bp = Blueprint('profile', __name__, url_prefix='/profile')


# User title part
@bp.route('/check-and-award-title')
def check_title():
    user_id = current_user.id
    result,status= check_and_award_title(user_id)
    return result,status


def has_title(user_id, title_name):
    if Title.query.filter_by(user_id=user_id, title=title_name).first():
        return True

def award_title(user_id:int, title:str):
    from app.models import Title
    if not has_title(user_id, title):
        new_title = Title(user_id=user_id, title=title, awarded_date=datetime.now())
        db.session.add(new_title)
        
        return True
    return False

def check_and_award_title(user_id:int, content=None):
    from app.models import User,Title,Post,Reply
    titles_awarded =[]
    user = User.query.filter_by(id=user_id).first()
    #  Newcomer--Register
    if user and not has_title(user_id, 'Newcomer'):
        if user.registered_date  >= datetime.now() - timedelta(days=1):
            award_title(user_id, 'Newcomer')
            titles_awarded.append('Newcomer')


    #  Community Pillar--Answer over 100 questions or posts
    replies = Reply.query.filter_by(user_id=user_id).count()
    if replies is not None and replies >= 100 and not has_title(user_id, 'Community Pillar'):
        award_title (user_id, 'Community Pillar')
        titles_awarded.append('Community Pillar')

    # Topic Expert--Post more than 50 times under a specific topic
    post_count_by_topic = Post.query.filter_by(user_id=user_id).group_by(Post.topic).count()
    if post_count_by_topic is not None  and post_count_by_topic >= 50 and not has_title(user_id, 'Topic Expert'):
        award_title(user_id, 'Topic Expert')
        titles_awarded.append('Topic Expert')

    # Influencer -- Accumulate over 500 votes on posts or replies
    total_votes = db.session.query(func.sum(Reply.votes)).filter_by(user_id=user_id).scalar()
    # total_votes = Reply.query.filter_by(user_id=user_id).sum(Reply.votes)
    if total_votes is not None and total_votes >= 500 and not has_title(user_id, 'Influencer'):
        award_title(user_id, 'Influencer')
        titles_awarded.append('Influencer')

    #  Night Owl -- Make over 20 posts during midnight hours
    night_posts = Post.query.filter_by(user_id=user_id).filter(Post.timestamp.between('00:00:00', '06:00:00')).count()
    if night_posts is not None and night_posts >= 20 and not has_title(user_id, 'Night Owl'):
        award_title (user_id, 'Night Owl')
        titles_awarded.append('Night Owl')

    #  Helping Hand -- Help other users solve problems and get marked as the “Accepted” more than 50 times
    accepted_replies = Reply.query.filter_by(user_id=user_id, accepted=True).count()
    if accepted_replies is not None and accepted_replies >= 50 and not has_title(user_id, 'Helping Hand'):
        award_title(user_id, 'Helping Hand')
        titles_awarded.append('Helping Hand')
    
    #  Explorer -- Post 5 topics at least once in each
    topic_count = Post.query \
    .filter_by(user_id=user_id) \
    .group_by(Post.topic) \
    .having(func.count(Post.id) >= 1) \
    .count()
    if topic_count is not None and topic_count>= 5 and not has_title(user_id, 'Explorer'):
        award_title(user_id, 'Explorer')
        titles_awarded.append('Explorer')


    #  Chatterbox King -- Post lenth more than 1000 characters
    if content is not None and  len(content) >= 1000 and not has_title(user_id, 'Chatterbox King'):
        award_title(user_id, 'Chatterbox King')
        titles_awarded.append('Chatterbox King')

    if titles_awarded:
        db.session.commit()
        return jsonify({'success': True, 'titles_awarded': titles_awarded}), 200
    else:
        return jsonify({'success': False, 'message': 'No titles awarded'}), 204  


# TODO: Page rendering and Api endpoints
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