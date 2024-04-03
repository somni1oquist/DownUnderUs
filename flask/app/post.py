from flask import Blueprint, jsonify, render_template, request, jsonify, request
from flask_login import current_user, login_required
from markupsafe import escape
from wtforms import Form, StringField
from wtforms.validators import Length, InputRequired
from app.models import Post, Reply, User, Vote
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
@bp.route('/create', methods=['GET', 'POST'])
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


#search part

# search view html
@bp.route('/search_view')
def show_search_view():
    return render_template('./post/search.html')

#validate the saerch input 

# set route
@bp.route('/search', methods=['GET'])

def search():
    query = request.args.get('q')
    sort_by = request.args.get('sort')
    filter_by = request.args.get('topic')
    if query and len(query) >= 3:
        # Search for posts title and body
        query_filter =Post.query.filter(
            db.or_(
           #ilike is case insensitive
            Post.body.ilike(f"%{query}%"),
            Post.title.ilike(f"%{query}%")
            )
        )
        
        # filter by topic
        if filter_by:
            query_filter = query_filter.filter(Post.topic == filter_by)
        
        # sort the results by views
        if sort_by == "views_desc":
            results = query_filter.order_by(Post.views.desc()).all()
        #  sort_by == "timestamp_desc" as default
        else:
            results = query_filter.order_by(Post.timestamp.desc()).all()

        # return the results
        posts = []
        for post in results:
            post_dict ={
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "topic": post.topic,
                "user_id": post.user_id,
                "views": post.views,
                "timestamp": post.timestamp,
                "username": User.query.get(post.user_id).username
            }
            posts.append(post_dict)
        return jsonify(posts)
    elif len(query) < 3 :
        return jsonify({"status":"error", "message": "Query too short"}), 400
    else:
        return jsonify({"status": "error", "message": "Missing query parameter"}), 400    

# Get post with replies
def load_post(id):
    '''Load post by id and return post with user and replies'''
    post = Post.query.get(id)
    if not post:
        return None
    post.user = User.query.get(post.user_id)
    # Sanitise body to prevent XSS
    post.body = escape(post.body)
    for reply in post.replies:
        reply.user = User.query.get(reply.user_id)
        reply.body = escape(reply.body)
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
    
    post.title = data.get('title')
    post.body = data.get('body')
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
    reply = Reply(body=body, post_id=post_id, user_id=current_user.id)
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

    reply.body = data.get('body')
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

    return jsonify(ResponseMessage.VOTED), 200

#posts filter in homepage
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
        'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'username': post.author.username
    } for post in posts]

    return jsonify(posts_data)

