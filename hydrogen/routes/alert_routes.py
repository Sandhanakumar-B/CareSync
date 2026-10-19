from flask import Blueprint, render_template, request, redirect, url_for, session
from routes.auth_routes import login_required
from database.db import query_db
from services.alert_service import resolve_alert

alert_bp = Blueprint('alert', __name__, url_prefix='/alerts')

@alert_bp.route('/')
@login_required
def list_alerts():
    alerts = query_db("""
        SELECT a.*, p.name as patient_name, u.full_name as resolved_by_name
        FROM alerts a
        LEFT JOIN patients p ON a.patient_id = p.id
        LEFT JOIN users u ON a.resolved_by = u.id
        ORDER BY a.timestamp DESC
    """)
    return render_template('alerts/list.html', alerts=alerts)

@alert_bp.route('/resolve/<int:alert_id>', methods=['POST'])
@login_required
def resolve(alert_id):
    notes = request.form.get('resolution_notes', '')
    resolve_alert(alert_id, session['user_id'], notes)
    return redirect(url_for('alert.list_alerts'))
