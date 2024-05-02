import os
from flask import Blueprint, render_template, request, redirect, send_from_directory, url_for
from flask_login import current_user, login_required
from .models import User, Post
from .tools import search_posts, json_response
from .enums import ResponseStatus
from werkzeug.utils import secure_filename
from app import db

# Define prefix for url
bp = Blueprint('index', __name__, url_prefix='/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint to handle image uploads
@bp.route('/upload/<int:profile_image>', methods=['POST'])
@login_required
def upload_image(profile_image):
    from flask import current_app as app
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Check if the request contains a file part
    if 'image' not in request.files:
        return json_response(ResponseStatus.ERROR, "No file part"), 400
    
    file = request.files['image']

    # Check if a file was actually selected
    if file.filename == '':
        return json_response(ResponseStatus.ERROR, "No selected file"), 400

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        filename = os.urandom(16).hex() + secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)  # Save the uploaded file

        # Update the user's profile image
        profile_image = bool(profile_image)
        if profile_image:
            # Remove the old profile image if it exists
            if current_user.profile_image:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], current_user.profile_image))
            current_user.profile_image = filename
            db.session.commit()
            return json_response(ResponseStatus.SUCCESS, "Profile image updated successfully", {"url": f"/uploads/{filename}"}), 200

        # Return the URL to access the uploaded file
        return json_response(ResponseStatus.SUCCESS, "Upload succeeded", {"url": f"/uploads/{filename}"}), 200
    
    return json_response(ResponseStatus.ERROR, "Invalid file type"), 400

@bp.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    from flask import current_app as app
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#search part
#  search api
@bp.route('/search')
def search():
    query = request.args.get('query')
    sort_by = request.args.get('sortBy')
    filter_by = request.args.get('topics')
    tags = request.args.get('tags') 
    # Search for posts title and body
    posts = search_posts(content=query, topics=filter_by, sort_by=sort_by, tags=tags)
    
    return render_template('./index/search.html', posts=posts)

@bp.route("/")
def index():
    # top 5 topics
    top_topics_data= db.session.query(
        Post.topic,
        # lable equals sql "as"
        db.func.sum(Post.views).label('total_views')
        ).group_by(Post.topic).order_by(db.desc('total_views')).limit(5).all()
    top_topics = [topic[0] for topic in top_topics_data]

    # top 5 tags
    # key is tag, value is total_views
    tag_views ={}
    posts = Post.query.with_entities(Post.tags, Post.views).all()
    for tags, views in posts:
        if tags is None:
            continue
        for tag in tags.split(','):
            tag = tag.strip()
            if tag not in tag_views:
                tag_views[tag] = 0
            tag_views[tag] += views
    top_tags_data = sorted(tag_views.items(), key=lambda x: x[1], reverse=True)[:5]
    top_tags = [tag for tag, views in top_tags_data]

    if current_user.is_authenticated:
    
        data = User.query.filter(User.username == current_user.username).first()
        # Force user to select interested topics if None
        if (data.interested_topics is None):
            return redirect(url_for('auth.topic_select'))
        
        default_topics = data.interested_topics.split(',')
        # Get the latest 10 interested posts
        posts = search_posts(topics=default_topics, sort_by='timestamp_desc', limit=10)
        return render_template('index.html', posts=posts,top_tags=top_tags, top_topics=top_topics)
    
    else:
        return render_template('index.html',top_topics=top_topics, top_tags=top_tags)




        


