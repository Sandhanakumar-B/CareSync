from flask import Blueprint, render_template
from routes.auth_routes import login_required
from database.db import query_db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')
