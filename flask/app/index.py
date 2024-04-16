from flask import Blueprint, jsonify, render_template, request, redirect, url_for,session
from flask_login import current_user, login_required
from app.models import Post, User
from app.tools import search_posts
from app import db

# Define prefix for url
bp = Blueprint('index', __name__, url_prefix='/')

#search part

#  search api
@bp.route('/search')
def search():
    query = request.args.get('query')
    sort_by = request.args.get('sort')
    filter_by = request.args.get('topic')
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




        


