from flask import Blueprint, jsonify, render_template, request, jsonify, url_for
from flask_login import current_user, login_required
from .forms import CreatePostForm
from .models import Post, Reply, Vote
from .enums import Topic, ResponseStatus, ResponseMessage
from .tools import json_response
from app import db

# Define prefix for url
bp = Blueprint('post', __name__, url_prefix='/post')

# Get topic list
@bp.route('/topics', methods=['GET'])
def topics():
    return jsonify({'topics': [topic.value for topic in Topic]})

# Create post
@bp.route('/create', methods=['POST'])
@login_required
def create():
    form = CreatePostForm(request.form)
    if form.validate():
        title = form.title.data
        body = form.body.data
        topic = form.topic.data
        tags = request.form.get('tags', None)
        location = form.location.data
        quest = Post(title=title, body=body, user_id=current_user.id, topic=topic, tags=tags, location=location)
        db.session.add(quest)
        db.session.commit()



        # return message
        return  json_response(ResponseStatus.SUCCESS, ResponseMessage.CREATED, {"post_id": quest.id}), 201
    else:
        errors = form.errors
        return json_response(ResponseStatus.ERROR, ResponseMessage.FORM_ERROR, {"errors": errors}), 400




# Get post with replies
def load_post(id):
    '''Load post by id and return post with user and replies'''
    post = Post.query.get(id)
    if not post:
        return None
    return post

def check_answer(replies):
    '''Check if any reply is accepted or has accepted replies'''
    if any(reply.accepted for reply in replies):
        return True
    elif any(reply.replies for reply in replies):
        return any(check_answer(reply.replies) for reply in replies)
    return False

def check_author(subject, user):
    '''Check if user is the author of a post or reply'''
    return subject.user_id == user.id

# Get post detail by id
@bp.route('/<int:post_id>', methods=['GET'])
def post(post_id):
    post = load_post(post_id)
    if not post:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    
    has_answer = check_answer(post.replies)

    # Increment view count
    if request.referrer != request.url:
        post.views += 1
    db.session.commit()

    return render_template("post/index.html", post=post, has_answer=has_answer)

# Edit post
@login_required
@bp.route('/<int:post_id>/edit', methods=['PUT'])
def edit(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return json_response(ResponseStatus.ERROR, ResponseMessage.UNAUTHORISED), 401
    
    # If location is not empty, update location only
    update_location = False
    location = data.get('location')
    if (location and location != 'null'):
        post.location = location
        update_location = True
    elif (location == 'null'):
        post.location = None
        update_location = True
    
    # If title is not None, update title only
    update_title = False
    title = data.get('title')
    if (title):
        post.title = title
        update_title = True
    
    if not update_location and not update_title:
        post.body = data.get('body') if data.get('body') else post.body
        post.tags = ','.join(data.get('tags')) if data.get('tags') else None

    db.session.commit()

    return json_response(ResponseStatus.SUCCESS, ResponseMessage.EDITED), 200

# Delete post
@login_required
@bp.route('/<int:post_id>/delete', methods=['DELETE'])
def delete(post_id):
    post = Post.query.get(post_id)

    if not post:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return json_response(ResponseStatus.ERROR, ResponseMessage.UNAUTHORISED), 401
    
    db.session.delete(post)
    db.session.commit()

    return json_response(ResponseStatus.SUCCESS, ResponseMessage.DELETED, {'redirect': url_for('index.index')}), 200

# Reply to a post
@login_required
@bp.route('/<int:post_id>/reply', methods=['POST'])
def reply(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404

    body = data.get('body')
    reply = Reply(body=body, post_id=post_id, user_id=current_user.id)
    db.session.add(reply)
    db.session.commit()



    return json_response(ResponseStatus.SUCCESS, ResponseMessage.REPLY_ADDED), 201

# Reply to a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>', methods=['POST'])
def reply_to_reply(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404

    body = data.get('body')
    reply = Reply(body=body, user_id=current_user.id, parent_id=reply_id)
    db.session.add(reply)
    db.session.commit()



    return json_response(ResponseStatus.SUCCESS, ResponseMessage.REPLY_ADDED), 201

# Accept a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/accept', methods=['PUT'])
def accept_reply(post_id, reply_id):
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return json_response(ResponseStatus.ERROR, ResponseMessage.UNAUTHORISED), 401

    reply.accepted = True
    db.session.commit()


    return json_response(ResponseStatus.SUCCESS, ResponseMessage.REPLY_ACCEPTED), 200

# Edit a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/edit', methods=['PUT'])
def edit_reply(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    elif not check_author(reply, current_user):
        return json_response(ResponseStatus.ERROR, ResponseMessage.UNAUTHORISED), 401

    reply.body = data.get('body')
    db.session.commit()

    return json_response(ResponseStatus.SUCCESS, ResponseMessage.REPLY_EDITED), 200

# Delete a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/delete', methods=['DELETE'])
def delete_reply(post_id, reply_id):
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    elif not check_author(reply, current_user):
        return json_response(ResponseStatus.ERROR, ResponseMessage.UNAUTHORISED), 401
    
    db.session.delete(reply)
    db.session.commit()

    return json_response(ResponseStatus.SUCCESS, ResponseMessage.REPLY_DELETED), 200

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
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    elif check_author(reply, current_user):
        return json_response(ResponseStatus.ERROR, ResponseMessage.UNAUTHORISED), 401
    # Check if user has already voted
    elif vote is not None:
        reply.votes -= 1
        db.session.delete(vote)
        db.session.commit()
    # If user has not voted, add vote and update reply
    else:
        reply.votes += 1
        db.session.add(Vote(user_id=current_user.id, reply_id=reply_id, vote_type=vote_type))
        db.session.commit()



    return json_response(ResponseStatus.SUCCESS, ResponseMessage.VOTED), 200

# Posts filter in portal
@login_required
@bp.route('/topics/<topic>', methods=['GET'])
def posts_by_topic(topic):
    posts = Post.query.filter_by(topic=topic).order_by(Post.timestamp.desc()).all()
    posts_data = [{
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'topic': post.topic,
        'user_id': post.user_id,
        'views': post.views,
        'timestamp': post.real_timestamp,
        'username': post.user.username
    } for post in posts]

    return jsonify(posts_data), 200

