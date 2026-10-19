from flask import Blueprint, render_template
from routes.auth_routes import login_required
from database.db import query_db

rfid_bp = Blueprint('rfid', __name__, url_prefix='/rfid')

@rfid_bp.route('/simulator')
@login_required
def simulator():
    patients = query_db("SELECT p.id, p.name, p.rfid_tag_id, p.medical_condition FROM patients p WHERE p.rfid_tag_id IS NOT NULL")
    readers = query_db("SELECT * FROM rfid_readers")
    return render_template('rfid/simulator.html', patients=patients, readers=readers)

@rfid_bp.route('/readers')
@login_required
def list_readers():
    readers = query_db("SELECT * FROM rfid_readers")
    return render_template('rfid/readers.html', readers=readers)

@rfid_bp.route('/tags')
@login_required
def list_tags():
    tags = query_db("""
        SELECT t.*, p.name as patient_name 
        FROM rfid_tags t 
        LEFT JOIN patients p ON t.assigned_patient_id = p.id
    """)
    return render_template('rfid/tags.html', tags=tags)
