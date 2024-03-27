from flask import Blueprint
from flask_login import login_required

# Define prefix for url
bp = Blueprint('profile', __name__, url_prefix='/profile')

# TODO: Page rendering and Api endpoints
@login_required
@bp.route('/', methods=['GET'])
def profile():
    return "Profile page"