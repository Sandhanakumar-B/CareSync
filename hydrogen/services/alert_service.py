from database.db import insert_db, query_db, update_db
from datetime import datetime

def check_and_trigger_alerts(patient_id, reader_id, tag_id, trigger_source):
    # Fetch patient details
    patient = query_db("SELECT * FROM patients WHERE id = ?", (patient_id,), one=True)
    if not patient:
        return None

    # Fetch reader details
    reader = query_db("SELECT * FROM rfid_readers WHERE reader_id = ?", (reader_id,), one=True)
    if not reader:
        return None

    alert_fired = False
    
    # Rule 1: Restricted zone access by wandering risk patient
    if reader['is_restricted'] == 1 and 'Wandering Risk' in (patient['medical_condition'] or ''):
        alert_code = f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{patient_id}"
        message = f"Wandering risk patient {patient['name']} entered restricted zone: {reader['location_name']}"
        insert_db("""
            INSERT INTO alerts (alert_code, patient_id, alert_type, location, severity, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (alert_code, patient['id'], 'Wandering', reader['location_name'], 'Critical', message))
        
        # Update patient status
        update_db("UPDATE patients SET status = 'Alert' WHERE id = ?", (patient_id,))
        alert_fired = True
        
    return alert_fired

def resolve_alert(alert_id, user_id, resolution_notes):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_db("""
        UPDATE alerts 
        SET status = 'Resolved', resolved_by = ?, resolution_notes = ?, resolved_at = ?
        WHERE id = ?
    """, (user_id, resolution_notes, now_str, alert_id))
    
    # Check if patient has any other active alerts, if not, reset status
    alert = query_db("SELECT patient_id FROM alerts WHERE id = ?", (alert_id,), one=True)
    if alert:
        active_alerts = query_db("SELECT id FROM alerts WHERE patient_id = ? AND status = 'Active'", (alert['patient_id'],))
        if not active_alerts:
            update_db("UPDATE patients SET status = 'Normal' WHERE id = ?", (alert['patient_id'],))
