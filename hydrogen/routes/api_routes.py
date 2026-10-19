from flask import Blueprint, jsonify, request
from database.db import query_db
from services.rfid_service import process_scan

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/rfid/scan', methods=['POST'])
def scan_rfid():
    data = request.json
    tag_id = data.get('tag_id')
    reader_id = data.get('reader_id')
    trigger_source = data.get('trigger_source', 'SIMULATION')
    notes = data.get('notes', '')
    
    if not tag_id or not reader_id:
        return jsonify({"success": False, "error": "Missing tag_id or reader_id"}), 400
        
    result = process_scan(tag_id, reader_id, trigger_source, notes)
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@api_bp.route('/dashboard/live-feed', methods=['GET'])
def live_feed():
    # recent_scans, stats, active_alerts, patients
    recent_scans = [dict(row) for row in query_db("""
        SELECT m.*, p.name as patient_name, r.location_name 
        FROM movement_logs m
        JOIN patients p ON m.patient_id = p.id
        JOIN rfid_readers r ON m.reader_id = r.reader_id
        ORDER BY m.timestamp DESC LIMIT 10
    """)]
    
    total_patients = query_db("SELECT COUNT(*) as count FROM patients", one=True)['count']
    
    active_alerts = [dict(row) for row in query_db("""
        SELECT a.*, p.name as patient_name 
        FROM alerts a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.status = 'Active'
        ORDER BY a.timestamp DESC
    """)]
    
    patients = [dict(row) for row in query_db("""
        SELECT id, name, patient_code, current_location, status, medical_condition, room_number, last_seen
        FROM patients
    """)]
    records = patients
    
    zone_occupancy = {}
    for p in patients:
        loc = p['current_location']
        if loc:
            zone_occupancy[loc] = zone_occupancy.get(loc, 0) + 1
            
    stats = {
        "total_patients": total_patients,
        "active_alerts_count": len(active_alerts),
        "zone_occupancy": zone_occupancy
    }
    
    return jsonify({
        "recent_scans": recent_scans,
        "stats": stats,
        "active_alerts": active_alerts,
        "patients": patients,
        "records": records
    })
