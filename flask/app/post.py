from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy.orm import subqueryload
from app import db
from app.models import Post, Reply, User

# Define prefix for url
bp = Blueprint('post', __name__, url_prefix='/post')

# Reponse messages
response = {
    'not_found': {'error': 'Post or reply not found'},
    'unauthorised': {'error': 'Unauthorised'},
    'created': {'message': 'Post created successfully'},
    'edited': {'message': 'Post edited successfully'},
    'deleted': {'message': 'Post deleted successfully'},
    'reply_added': {'message': 'Reply added successfully'},
    'reply_edited': {'message': 'Reply edited successfully'},
    'reply_deleted': {'message': 'Reply deleted successfully'},
    'vote': {'message': 'Vote successful'}
}

# Get post with replies
def load_post(id):
    post = Post.query.get(id)
    if not post:
        return None
    post.user = User.query.get(post.user_id)
    for reply in post.replies:
        reply.user = User.query.get(reply.user_id)
    return post

# Check if user is author of post/reply
def check_author(subject, user):
    return subject.user_id == user.id

# Get post detail by id
@bp.route('/<int:post_id>', methods=['GET'])
def post(post_id):
    post = load_post(post_id)
    if not post:
        return jsonify(response['not_found']), 404
    return render_template("post/index.html", post=post)

# Edit post
@login_required
@bp.route('/<int:post_id>/edit', methods=['PUT'])
def edit(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return jsonify(response['not_found']), 404
    elif not check_author(post, current_user):
        return jsonify(response['unauthorised']), 403
    
    post.title = data.get('title')
    post.body = data.get('body')
    db.session.commit()

    return jsonify(response['edited']), 200

# Delete post
@login_required
@bp.route('/<int:post_id>/delete', methods=['DELETE'])
def delete(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify(response['not_found']), 404
    elif not check_author(post, current_user):
        return jsonify(response['unauthorised']), 403
    
    db.session.delete(post)
    db.session.commit()

    return jsonify(response['deleted']), 200

# Reply to a post
@login_required
@bp.route('/<int:post_id>/reply', methods=['POST'])
def reply(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return jsonify(response['not_found']), 404

    body = data.get('body')
    reply = Reply(body=body, post_id=post_id)
    db.session.add(reply)
    db.session.commit()

    return jsonify(response['reply_added']), 201

# Edit a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/edit', methods=['PUT'])
def edit_reply(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return jsonify(response['not_found']), 404
    elif not check_author(reply, current_user):
        return jsonify(response['unauthorised']), 403

    reply.body = data.get('body')
    db.session.commit()

    return jsonify(response['reply_edited']), 200

# Delete a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/delete', methods=['DELETE'])
def delete_reply(post_id, reply_id):
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return jsonify(response['not_found']), 404
    elif not check_author(reply, current_user):
        return jsonify(response['unauthorised']), 403
    
    db.session.delete(reply)
    db.session.commit()

    return jsonify(response['reply_deleted']), 200

# Vote on a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/vote', methods=['PUT'])
def vote(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return jsonify(response['not_found']), 404
    elif not check_author(reply, current_user):
        return jsonify(response['unauthorised']), 403

    vote = int(data.get('vote'))
    reply.votes += vote
    db.session.commit()

    return jsonify(response['vote']), 200
