from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy.orm import lazyload
from app import db
from app.models import Post, Reply

# Define prefix for url
bp = Blueprint('post', __name__, url_prefix='/post')

# Get post with replies
def get_post(id):
    post = Post.query.options(lazyload(Post.replies)).get(id)
    return post

# Check if user is author of post/reply
def check_author(subject, user):
    return subject.user_id == user.id

# Get post detail by id
@bp.route('/<int:post_id>', methods=['GET'])
def post(post_id):
    post = get_post(post_id)
    return render_template("post/index.html", post=post)

# Edit post
@login_required
@bp.route('/<int:post_id>/edit', methods=['PUT'])
def edit(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return 404
    elif not check_author(post, current_user):
        return 403
    
    post.title = data.get('title')
    post.body = data.get('body')
    db.session.commit()

    return 201

# Delete post
@login_required
@bp.route('/<int:post_id>/delete', methods=['DELETE'])
def delete(post_id):
    post = Post.query.get(post_id)

    if not post:
        return 404
    elif not check_author(post, current_user):
        return 403
    
    db.session.delete(post)

# Reply to a post
@login_required
@bp.route('/<int:post_id>/reply', methods=['POST'])
def reply(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return 404

    body = data.get('body')
    reply = Reply(body=body, post_id=post_id)
    db.session.add(reply)
    db.session.commit()

    return 201

# Edit a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/edit', methods=['PUT'])
def edit_reply(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return 404
    elif not check_author(reply, current_user):
        return 403

    reply.body = data.get('body')
    db.session.commit()

    return 201

# Delete a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/delete', methods=['DELETE'])
def delete_reply(post_id, reply_id):
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return 404
    elif not check_author(reply, current_user):
        return 403
    
    db.session.delete(reply)

    return 201

# Vote on a reply
@login_required
@bp.route('/<int:post_id>/reply/<int:reply_id>/vote', methods=['POST'])
def vote(post_id, reply_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    reply = Reply.query.get(reply_id)

    if not post or not reply:
        return 404

    vote = data.get('vote')
    reply.votes += vote
    db.session.commit()

    return 201
