from enum import Enum
from flask import Blueprint, jsonify, render_template, request, redirect, flash, jsonify, request
from flask_login import current_user, login_required, current_user
import wtforms
from wtforms.validators import length
from wtforms import validators
from sqlalchemy.orm import subqueryload
from app.models import Post, Reply, User, Vote
from app.enum import Topic, ResponseMessage
from app import db

# Define prefix for url
bp = Blueprint('post', __name__, url_prefix='/post')

#validate the form
class QuestForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3,max=100, message="Title fromatting error!!")])
    body = wtforms.StringField(validators=[length(min=3,message="Content fromatting error!!")])
    topic = wtforms.StringField(validators=[validators.InputRequired(message="Please select a topic!!")])

# Get topic list
@bp.route('/topics', methods=['GET'])
def get_topic():
    return jsonify([topic.value for topic in Topic])

# Create post
@bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'GET':
        return render_template('post/create-post.html', current_user=current_user)
    
    form = QuestForm(request.form)
    if form.validate():
        title = form.title.data
        body = form.body.data
        topic = form.topic.data
        quest = Post(title=title, body=body, user_id=current_user.id, topic=topic)
        db.session.add(quest)
        db.session.commit()
        # return message
        return jsonify({"status":"success", "message": "Post created successfully", "post_id": quest.id}), 201
    else:
        errors = form.errors
        return jsonify({"status":"error", "message": "Validation failed", "errors": errors}), 400

def load_post(id):
    '''Load post by id and return post with user and replies'''
    post = Post.query.get(id)
    if not post:
        return None
    post.user = User.query.get(post.user_id)
    for reply in post.replies:
        reply.user = User.query.get(reply.user_id)
    return post

def check_author(subject, user):
    '''Check if user is the author of a post or reply'''
    return subject.user_id == user.id

# Get post detail by id
@bp.route('/<int:post_id>', methods=['GET'])
def post(post_id):
    post = load_post(post_id)
    if not post:
        return jsonify(ResponseMessage.NOT_FOUND), 404
    
    # Increment view count
    post.views += 1
    db.session.commit()

    return render_template("post/index.html", post=post)

# Edit post
@login_required
@bp.route('/<int:post_id>/edit', methods=['PUT'])
def edit(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return jsonify(ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return jsonify(ResponseMessage.UNAUTHORISED), 403
    
    post.title = data.get('title')
    post.body = data.get('body')
    db.session.commit()

    return jsonify(ResponseMessage.EDITED), 200

# Delete post
@login_required
@bp.route('/<int:post_id>/delete', methods=['DELETE'])
def delete(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify(ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return jsonify(ResponseMessage.UNAUTHORISED), 403
    
    db.session.delete(post)
    db.session.commit()

    return jsonify(ResponseMessage.DELETED]), 200

# Reply to a post
@login_required
@bp.route('/<int:post_id>/reply', methods=['POST'])
def reply(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return jsonify(ResponseMessage.NOT_FOUND), 404

    body = data.get('body')
    reply = Reply(body=body, post_id=post_id, user_id=current_user.id)
    db.session.add(reply)
    db.session.commit()

    return jsonify(ResponseMessage.REPLY_ADDED), 201

# Accept a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/accept', methods=['PUT'])
def accept_reply(post_id, reply_id):
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return jsonify(ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return jsonify(ResponseMessage.UNAUTHORISED), 403

    reply.accepted = True
    db.session.commit()

    return jsonify(ResponseMessage.REPLY_ACCEPTED), 200

# Edit a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/edit', methods=['PUT'])
def edit_reply(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return jsonify(ResponseMessage.NOT_FOUND), 404
    elif not check_author(reply, current_user):
        return jsonify(ResponseMessage.UNAUTHORISED), 403

    reply.body = data.get('body')
    db.session.commit()

    return jsonify(ResponseMessage.REPLY_EDITED), 200

# Delete a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/delete', methods=['DELETE'])
def delete_reply(post_id, reply_id):
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return jsonify(ResponseMessage.NOT_FOUND), 404
    elif not check_author(reply, current_user):
        return jsonify(ResponseMessage.UNAUTHORISED), 403
    
    db.session.delete(reply)
    db.session.commit()

    return jsonify(ResponseMessage.REPLY_DELETED), 200

# Vote on a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/vote', methods=['POST'])
def vote(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)
    vote = Vote.query.filter_by(user_id=current_user.id, reply_id=reply_id).first()
    vote_type = data.get('vote')

    if not post or not reply:
        return jsonify(ResponseMessage.NOT_FOUND), 404
    elif check_author(reply, current_user):
        return jsonify(ResponseMessage.UNAUTHORISED), 403
    # Check if user has already voted
    elif vote is not None:
        # If same vote type, revoke vote and update reply
        if vote.vote_type == vote_type:
            reply.votes += 1 if vote_type == 'downvote' else -1
            db.session.delete(vote)
            db.session.commit()
            return jsonify(ResponseMessage.VOTE_REVOKED), 200
        # Else, update vote and reply
        else:
            vote.vote_type = vote_type
            reply.votes += 2 if vote_type == 'upvote' else -2
            db.session.commit()
            return jsonify(ResponseMessage.VOTE_UPDATED), 200
    # If user has not voted, add vote and update reply
    reply.votes += 1 if vote_type == 'upvote' else -1
    db.session.add(Vote(user_id=current_user.id, reply_id=reply_id, vote_type=vote_type))
    db.session.commit()

    return jsonify(ResponseMessage.VOTED), 200
