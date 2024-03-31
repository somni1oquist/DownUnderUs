from flask import Blueprint, render_template, request, redirect, flash, jsonify
from flask_login import login_required, current_user
import wtforms
from wtforms.validators import length
from wtforms import validators
from sqlalchemy.orm import lazyload
from app.models import Post
from app import db

# Define prefix for url
bp = Blueprint('post', __name__, url_prefix='/post')

# create post part
@bp.route('/show-create-post')
def show_create_post():
   
    return render_template('./post/create-post.html')

#validate the form
class Quest_form(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3,max=100, message="Title fromatting error!!")])
    body = wtforms.StringField(validators=[length(min=3,message="Content fromatting error!!")])
    topic = wtforms.StringField(validators=[validators.InputRequired(message="Please select a topic!!")])

# set route
@bp.route('/create_post', methods=['GET', 'POST'])

#decorator for login
@login_required

def create_post():
    form = Quest_form(request.form)
    if form.validate():
        title = form.title.data
        body = form.body.data
        topic = form.topic.data
        quest = Post(title=title, body=body, user_id=current_user.id, topic=topic)
        db.session.add(quest)
        db.session.commit()
        # return message
        return jsonify({"status":"success", "message": "Post created successfully"})
    else:
        errors = form.errors
        return jsonify({"status":"error", "message": "Validation failed", "errors": errors}), 400

# get user name
@bp.route('/get_user_name')
def get_user_name():
    if current_user.is_authenticated:
        return jsonify(username=current_user.username)
    else:
        return jsonify({"error": "User not logged in"}), 401


def get_post(id):
    # Get post with replies
    post = Post.query.options(lazyload(Post.replies)).get(id)
    return post

# Get post detail by id
@bp.route('/<int:id>', methods=['GET'])
def post(id):
    post = get_post(id)
    return render_template("post/index.html", post=post)

# Reply to a post
@login_required
@bp.route('/<int:id>/reply', methods=['POST'])
def reply():
    pass

# Vote on a reply
@login_required
@bp.route('/<int:id>/reply/<int:reply_id>/vote', methods=['POST'])
def vote():
    pass