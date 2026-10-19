from flask import Blueprint, render_template
from routes.auth_routes import login_required

map_bp = Blueprint('map', __name__, url_prefix='/rfid')

@map_bp.route('/facility-map')
@login_required
def facility_map():
    return render_template('map/index.html')
