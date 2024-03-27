from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy.orm import lazyload
from app.models import Post

# Define prefix for url
bp = Blueprint('post', __name__, url_prefix='/post')

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