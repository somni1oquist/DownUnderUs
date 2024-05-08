from flask import Blueprint, jsonify, render_template, request, jsonify, session, url_for
from flask_login import current_user, login_required
from .forms import CreatePostForm
from .models import Post, Reply, Vote
from .enums import Topic, ResponseStatus, ResponseMessage
from .tools import json_response, update_user_points
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
        update_user_points(current_user.id,15)
        db.session.commit()

        # return message
        return  json_response(ResponseStatus.SUCCESS, ResponseMessage.CREATED, {"post_id": quest.id,'points_added': 15}), 201
    else:
        errors = form.errors
        return json_response(ResponseStatus.ERROR, ResponseMessage.FORM_ERROR, {"errors": errors}), 400

def check_answer(replies):
    '''Check if any reply is accepted or has accepted replies'''
    stack = [reply for reply in replies]
    while stack:
        current_reply = stack.pop()
        if current_reply.accepted:
            return True
        
        if current_reply.replies:
            stack.extend(current_reply.replies)

    return False

def check_author(subject, user):
    '''Check if user is the author of a post or reply'''
    return subject.user_id == user.id

# Get post detail by id
@bp.route('/<int:post_id>', methods=['GET'])
def post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    
    has_answer = check_answer(post.replies)

    # Increment view count
    if 'viewed_posts' not in session:
        session['viewed_posts'] = []
    if post_id not in session['viewed_posts']:
        post.views += 1
        session['viewed_posts'].append(post_id)
        session.update()
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
    if title and len(title) >= 3:
        post.title = title
        update_title = True

    body = data.get('body')
    # TODO: Use RegEx to check malicious code in body e.g., <script>
    if len(body) < 10 or len(title) < 3:
        return json_response(ResponseStatus.ERROR, 'Please enter proper contents.'), 400
    
    if not update_location and not update_title:
        post.body = body
        # TODO: Check after clearing tags
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
    update_user_points(current_user.id, 10)

    return json_response(ResponseStatus.SUCCESS, ResponseMessage.REPLY_ADDED,{'points_added': 10}), 201

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

    # Check if post has an answer
    if check_answer(post.replies):
        return json_response(ResponseStatus.ERROR, 'The post already has an answer.'), 403

    reply.accepted = True
    update_user_points(reply.user_id, 30)
    db.session.commit()


    return json_response(ResponseStatus.SUCCESS, ResponseMessage.REPLY_ACCEPTED), 200

# Edit a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/edit', methods=['PUT'])
def edit_reply(post_id, reply_id):
    data = request.get_json()
    body = data.get('body')
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return json_response(ResponseStatus.ERROR, ResponseMessage.NOT_FOUND), 404
    elif not check_author(reply, current_user):
        return json_response(ResponseStatus.ERROR, ResponseMessage.UNAUTHORISED), 401

    # Check body
    # TODO: Use RegEx to check malicious code e.g., <script>
    if (len(body) < 10):
        return json_response(ResponseStatus.ERROR, 'Please enter valid content.'), 400

    reply.body = body
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
        return json_response(ResponseStatus.SUCCESS, ResponseMessage.VOTE_REVOKED), 200
    # If user has not voted, add vote and update reply
    reply.votes += 1
    db.session.add(Vote(user_id=current_user.id, reply_id=reply_id, vote_type=vote_type))
    db.session.commit()

    return json_response(ResponseStatus.SUCCESS, ResponseMessage.VOTED), 200

