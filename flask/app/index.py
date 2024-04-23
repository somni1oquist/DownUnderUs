import os
from flask import Blueprint, render_template, request, redirect, send_from_directory, url_for
from flask_login import current_user, login_required
from app.models import User
from app.tools import search_posts, json_response
from app.enums import ResponseStatus
from werkzeug.utils import secure_filename

# Define prefix for url
bp = Blueprint('index', __name__, url_prefix='/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint to handle image uploads
@bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
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
    # Search for posts title and body
    posts = search_posts(content=query, topics=filter_by, sort_by=sort_by)
    
    return render_template('./index/search.html', posts=posts)

@bp.route("/")
def index():
    if current_user.is_authenticated:
    
        data = User.query.filter(User.username == current_user.username).first()
        # Force user to select interested topics if None
        if (data.interested_topics is None):
            return redirect(url_for('auth.topic_select'))
        
        default_topics = data.interested_topics.split(',')
        # Get the latest 10 interested posts
        posts = search_posts(topics=default_topics, sort_by='timestamp_desc', limit=10)
        return render_template('index.html', posts=posts)
    
    else:
        return render_template('index.html')




        


