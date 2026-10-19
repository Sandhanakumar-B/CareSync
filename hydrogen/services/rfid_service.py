from database.db import query_db, insert_db, update_db
from services.alert_service import check_and_trigger_alerts
from datetime import datetime

def process_scan(tag_id, reader_id, trigger_source, notes=""):
    # Find tag and patient
    tag = query_db("SELECT * FROM rfid_tags WHERE tag_id = ?", (tag_id,), one=True)
    if not tag or not tag['assigned_patient_id']:
        return {"success": False, "error": "Tag not assigned to any patient"}
    
    patient_id = tag['assigned_patient_id']
    patient = query_db("SELECT * FROM patients WHERE id = ?", (patient_id,), one=True)
    
    # Find reader
    reader = query_db("SELECT * FROM rfid_readers WHERE reader_id = ?", (reader_id,), one=True)
    if not reader:
        return {"success": False, "error": "Invalid reader ID"}
        
    location = reader['location_name']
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update patient
    update_db("""
        UPDATE patients 
        SET current_location = ?, last_seen = ? 
        WHERE id = ?
    """, (location, now_str, patient_id))
    
    # Insert movement log
    insert_db("""
        INSERT INTO movement_logs (patient_id, rfid_tag_id, reader_id, location, timestamp, trigger_source, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (patient_id, tag_id, reader_id, location, now_str, trigger_source, notes))
    
    # Check for alerts
    alert_fired = check_and_trigger_alerts(patient_id, reader_id, tag_id, trigger_source)
    
    return {
        "success": True,
        "patient_name": patient['name'],
        "location": location,
        "alert_fired": alert_fired
    }
