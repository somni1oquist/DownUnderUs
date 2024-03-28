from flask import Blueprint, request, render_template


# Define prefix for url
bp = Blueprint('create_post', __name__, url_prefix='/')

@bp.route("/publish")
def publish():
    return render_template("post/create-post.html")

