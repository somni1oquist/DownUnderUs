from flask import Blueprint, jsonify, render_template, request, jsonify
from flask_login import current_user, login_required
from markupsafe import escape
from wtforms import Form, StringField
from wtforms.validators import Length, InputRequired
from app.models import Post, Reply, Vote
from app.enums import Topic, ResponseMessage
from app import db

# Define prefix for url
bp = Blueprint('post', __name__, url_prefix='/post')

# Validate the form
class QuestForm(Form):
    title = StringField(validators=[Length(min=3,max=100, message="Title fromatting error!!")])
    body = StringField(validators=[Length(min=3,message="Content fromatting error!!")])
    topic = StringField(validators=[InputRequired(message="Please select a topic!!")])

# Get topic list
@bp.route('/topics', methods=['GET'])
def topics():
    return jsonify([topic.value for topic in Topic])

# Create post
@bp.route('/create', methods=['POST'])
@login_required
def create():
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




# Get post with replies
def load_post(id):
    '''Load post by id and return post with user and replies'''
    post = Post.query.get(id)
    if not post:
        return None
    return post

def check_author(subject, user):
    '''Check if user is the author of a post or reply'''
    return subject.user_id == user.id

def load_message(message):
    '''Load message and return as json response'''
    return jsonify({"message": message})

# Get post detail by id
@bp.route('/<int:post_id>', methods=['GET'])
def post(post_id):
    post = load_post(post_id)
    if not post:
        return load_message(ResponseMessage.NOT_FOUND), 404
    
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
        return load_message(ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return load_message(ResponseMessage.UNAUTHORISED), 403
    
    post.title = escape(data.get('title'))
    post.body = escape(data.get('body'))
    db.session.commit()

    return jsonify(ResponseMessage.EDITED.value), 200

# Delete post
@login_required
@bp.route('/<int:post_id>/delete', methods=['DELETE'])
def delete(post_id):
    post = Post.query.get(post_id)

    if not post:
        return load_message(ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return load_message(ResponseMessage.UNAUTHORISED), 403
    
    db.session.delete(post)
    db.session.commit()

    return load_message(ResponseMessage.DELETED), 200

# Reply to a post
@login_required
@bp.route('/<int:post_id>/reply', methods=['POST'])
def reply(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return load_message(ResponseMessage.NOT_FOUND), 404

    body = data.get('body')
    reply = Reply(body=escape(body), post_id=post_id, user_id=current_user.id)
    db.session.add(reply)
    db.session.commit()

    return load_message(ResponseMessage.REPLY_ADDED), 201

# Reply to a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>', methods=['POST'])
def reply_to_reply(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return load_message(ResponseMessage.NOT_FOUND), 404

    body = data.get('body')
    reply = Reply(body=escape(body), user_id=current_user.id, parent_id=reply_id)
    db.session.add(reply)
    db.session.commit()

    return load_message(ResponseMessage.REPLY_ADDED), 201

# Accept a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/accept', methods=['PUT'])
def accept_reply(post_id, reply_id):
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return load_message(ResponseMessage.NOT_FOUND), 404
    elif not check_author(post, current_user):
        return load_message(ResponseMessage.UNAUTHORISED), 403

    reply.accepted = True
    db.session.commit()

    return load_message(ResponseMessage.REPLY_ACCEPTED), 200

# Edit a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/edit', methods=['PUT'])
def edit_reply(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return load_message(ResponseMessage.NOT_FOUND), 404
    elif not check_author(reply, current_user):
        return load_message(ResponseMessage.UNAUTHORISED), 403

    reply.body = escape(data.get('body'))
    db.session.commit()

    return load_message(ResponseMessage.REPLY_EDITED), 200

# Delete a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/delete', methods=['DELETE'])
def delete_reply(post_id, reply_id):
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return load_message(ResponseMessage.NOT_FOUND), 404
    elif not check_author(reply, current_user):
        return load_message(ResponseMessage.UNAUTHORISED), 403
    
    db.session.delete(reply)
    db.session.commit()

    return load_message(ResponseMessage.REPLY_DELETED), 200

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
        return load_message(ResponseMessage.NOT_FOUND), 404
    elif check_author(reply, current_user):
        return load_message(ResponseMessage.UNAUTHORISED), 403
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

    return load_message(ResponseMessage.VOTED), 200

# Posts filter in portal
@login_required
@bp.route('/topics/<string:topic>', methods=['GET'])
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

