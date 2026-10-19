from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.auth_routes import login_required
from database.db import query_db, insert_db, update_db

patient_bp = Blueprint('patient', __name__, url_prefix='/patients')

@patient_bp.route('/')
@login_required
def list_patients():
    patients = query_db("""
        SELECT p.*, t.tag_label, u.full_name as caregiver_name 
        FROM patients p 
        LEFT JOIN rfid_tags t ON p.rfid_tag_id = t.tag_id
        LEFT JOIN users u ON p.assigned_caregiver_id = u.id
    """)
    return render_template('patients/list.html', patients=patients)

@patient_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    if session.get('role') != 'admin':
        flash('Only admins can add new patient records.', 'error')
        return redirect(url_for('patient.list_patients'))

    caregivers = query_db("""
        SELECT id, full_name
        FROM users
        WHERE role IN ('admin', 'caregiver')
        ORDER BY full_name
    """)

    if request.method == 'POST':
        patient_code = request.form.get('patient_code', '').strip()
        name = request.form.get('name', '').strip()

        if not patient_code or not name:
            flash('Patient code and name are required.', 'error')
            return render_template('patients/new.html', caregivers=caregivers, form=request.form)

        age = request.form.get('age', '').strip()
        if age:
            try:
                age = int(age)
            except ValueError:
                flash('Age must be a valid number.', 'error')
                return render_template('patients/new.html', caregivers=caregivers, form=request.form)
        else:
            age = None

        caregiver_id = request.form.get('assigned_caregiver_id', '').strip() or None
        if caregiver_id is not None:
            caregiver_id = int(caregiver_id)

        rfid_tag_id = request.form.get('rfid_tag_id', '').strip() or None
        current_location = request.form.get('current_location', '').strip() or None
        room_number = request.form.get('room_number', '').strip() or None
        status = request.form.get('status', 'Normal').strip() or 'Normal'
        gender = request.form.get('gender', '').strip() or None
        medical_condition = request.form.get('medical_condition', '').strip() or None
        emergency_contact = request.form.get('emergency_contact', '').strip() or None
        notes = request.form.get('notes', '').strip() or None

        try:
            insert_db("""
                INSERT INTO patients (
                    patient_code, name, age, gender, medical_condition,
                    rfid_tag_id, assigned_caregiver_id, current_location,
                    room_number, status, emergency_contact, notes, last_seen
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                patient_code,
                name,
                age,
                gender,
                medical_condition,
                rfid_tag_id,
                caregiver_id,
                current_location,
                room_number,
                status,
                emergency_contact,
                notes,
            ))
        except Exception:
            flash('That patient code already exists or the record could not be saved.', 'error')
            return render_template('patients/new.html', caregivers=caregivers, form=request.form)

        flash('Patient record created successfully.', 'success')
        return redirect(url_for('patient.list_patients'))

    return render_template('patients/new.html', caregivers=caregivers, form=None)

@patient_bp.route('/<int:id>')
@login_required
def view_profile(id):
    patient = query_db("""
        SELECT p.*, t.tag_label, u.full_name as caregiver_name 
        FROM patients p 
        LEFT JOIN rfid_tags t ON p.rfid_tag_id = t.tag_id
        LEFT JOIN users u ON p.assigned_caregiver_id = u.id
        WHERE p.id = ?
    """, (id,), one=True)
    
    movement_logs = query_db("""
        SELECT m.*, r.location_name
        FROM movement_logs m
        JOIN rfid_readers r ON m.reader_id = r.reader_id
        WHERE m.patient_id = ?
        ORDER BY m.timestamp DESC LIMIT 50
    """, (id,))
    
    alerts = query_db("""
        SELECT * FROM alerts WHERE patient_id = ? ORDER BY timestamp DESC LIMIT 10
    """, (id,))
    
    return render_template('patients/profile.html', patient=patient, movement_logs=movement_logs, alerts=alerts)
