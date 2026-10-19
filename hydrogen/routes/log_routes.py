from flask import Blueprint, render_template
from routes.auth_routes import login_required
from database.db import query_db

log_bp = Blueprint('log', __name__, url_prefix='/logs')

@log_bp.route('/')
@login_required
def list_logs():
    logs = query_db("""
        SELECT m.*, p.name as patient_name, r.location_name
        FROM movement_logs m
        JOIN patients p ON m.patient_id = p.id
        JOIN rfid_readers r ON m.reader_id = r.reader_id
        ORDER BY m.timestamp DESC
    """)
    return render_template('logs/list.html', logs=logs)
