from flask import Blueprint
from flask_login import login_required


bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# TODO: Page rendering and Api endpoints
@login_required
@bp.route('/', methods=['GET'])
def dashboard():
    return "Dashboard page"