from flask import Blueprint, jsonify, render_template, request, redirect, url_for,session
from flask_login import current_user, login_required
from app.models import Post, User
from app import db

# Define prefix for url
bp = Blueprint('index', __name__, url_prefix='/')

#search part

#  search api
@bp.route('/search', methods=['GET', 'POST'])

def search():
    query = request.args.get('query')
    sort_by = request.args.get('sort')
    filter_by = request.args.get('topic')

    # if query and len(query) >= 3:
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
            "timestamp": post.real_timestamp,
            "username": post.user.username
        }
        posts.append(post_dict)
    session['search_results'] = posts
    return render_template('./index/search.html', posts=posts)
    # return jsonify(posts)
    # elif len(query) < 3 :
    #     return jsonify({"status":"error", "message": "Query too short"}), 400
    # else:
    #     return jsonify({"status": "error", "message": "Missing query parameter"}), 400    

@bp.route('/search/filter', methods=['GET'])
def filter_search_result():
    filter=request.args.get('topic')
    search_results = session.get('search_results')
    filtered_results = []
    for result in search_results:
        if result['topic'] == filter:
            filtered_results.append(result)
    return render_template('./index/search.html', posts=filtered_results)

@bp.route('/search/sort', methods=['GET'])
def sort_search_result():
    sort=request.args.get('sort')
    search_results = session.get('search_results')

    if sort == 'views_desc':
        sorted_results = sorted(search_results, key=lambda x: x['views'], reverse=True)
    else:
        sorted_results = sorted(search_results, key=lambda x: x['timestamp'], reverse=True)
    return render_template('./index/search.html', posts=sorted_results)



@bp.route("/")
def index():
    if current_user.is_authenticated:
    
        data = User.query.filter(User.username == current_user.username).first()
        # Force user to select interested topics if None
        if (data.interested_topics is None):
            return redirect(url_for('auth.topic_select'))
        
        default_topics = data.interested_topics.split(',')

        # dynamic construction features
        default_results = Post.query.filter(
            Post.topic.in_(default_topics)
        ).order_by(Post.timestamp.desc()).all()
        posts = []
        for post in default_results:
            post_dict = {
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "topic": post.topic,
                "user_id": post.user_id,
                "views": post.views,
                "timestamp": post.real_timestamp,
                "username": post.user.username
            }
            posts.append(post_dict)
        return render_template('index.html', posts=posts)
    
    else:
        return render_template('index.html')




        


