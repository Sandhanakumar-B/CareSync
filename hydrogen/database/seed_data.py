import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'caresync.db')
SCHEMA = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_db():
    print("Initializing database...")
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    
    conn = sqlite3.connect(DATABASE)
    with open(SCHEMA, 'r') as f:
        conn.executescript(f.read())
    
    cursor = conn.cursor()

    # Seed Users
    print("Seeding users...")
    admin_pw = generate_password_hash("admin123")
    caregiver_pw = generate_password_hash("caregiver123")
    
    users = [
        ("admin", "admin@caresync.local", admin_pw, "admin", "Admin User", "555-0100"),
        ("caregiver", "caregiver@caresync.local", caregiver_pw, "caregiver", "Jane Smith", "555-0101"),
        ("caregiver2", "caregiver2@caresync.local", caregiver_pw, "caregiver", "John Doe", "555-0102")
    ]
    cursor.executemany("""
        INSERT INTO users (username, email, password_hash, role, full_name, phone) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, users)

    # Seed RFID Readers
    print("Seeding RFID readers...")
    readers = [
        ("READER-01", "Patient Room", 0, "Active", "General patient ward"),
        ("READER-02", "Therapy Room", 0, "Active", "Physical therapy area"),
        ("READER-03", "Dining Hall", 0, "Active", "Main dining hall"),
        ("READER-04", "Medical Room", 1, "Active", "Restricted access medical supplies"),
        ("READER-05", "Main Entrance", 1, "Active", "Restricted perimeter gate")
    ]
    cursor.executemany("""
        INSERT INTO rfid_readers (reader_id, location_name, is_restricted, status, description) 
        VALUES (?, ?, ?, ?, ?)
    """, readers)

    # Seed RFID Tags
    print("Seeding RFID tags...")
    tags = [
        ("RFID001", "Tag 1", "Assigned", 1),
        ("RFID002", "Tag 2", "Assigned", 2),
        ("RFID003", "Tag 3", "Assigned", 3),
        ("RFID004", "Tag 4", "Assigned", 4),
        ("RFID005", "Tag 5", "Assigned", 5),
        ("RFID006", "Tag 6", "Available", None),
        ("RFID007", "Tag 7", "Available", None)
    ]
    cursor.executemany("""
        INSERT INTO rfid_tags (tag_id, tag_label, status, assigned_patient_id) 
        VALUES (?, ?, ?, ?)
    """, tags)

    # Seed Patients
    print("Seeding patients...")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    patients = [
        ("PT-001", "Alice Johnson", 78, "Female", "Mild Dementia - Wandering Risk", "RFID001", 2, "Patient Room", "101A", "Attention Required", "Bob Johnson (555-0201)", "Requires regular check-ins.", now_str),
        ("PT-002", "Robert Williams", 82, "Male", "Alzheimer's Disease - Wandering Risk", "RFID002", 2, "Dining Hall", "102B", "Normal", "Mary Williams (555-0202)", "High risk of wandering.", now_str),
        ("PT-003", "Eva Martinez", 65, "Female", "Post-Op Recovery", "RFID003", 3, "Therapy Room", "103A", "Normal", "Carlos Martinez (555-0203)", "Needs assistance with mobility.", now_str),
        ("PT-004", "David Lee", 70, "Male", "Cardiac Monitoring", "RFID004", 3, "Patient Room", "104B", "Normal", "Susan Lee (555-0204)", "Regular BP checks.", now_str),
        ("PT-005", "Martha White", 88, "Female", "General Frailty", "RFID005", 2, "Dining Hall", "105A", "Normal", "Jim White (555-0205)", "Fall risk.", now_str)
    ]
    cursor.executemany("""
        INSERT INTO patients (patient_code, name, age, gender, medical_condition, rfid_tag_id, assigned_caregiver_id, current_location, room_number, status, emergency_contact, notes, last_seen) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, patients)

    # Seed initial movement logs
    print("Seeding movement logs...")
    logs = [
        (1, "RFID001", "READER-01", "Patient Room", (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"), "SIMULATION", "Initial scan"),
        (2, "RFID002", "READER-03", "Dining Hall", (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"), "SIMULATION", "Initial scan"),
        (3, "RFID003", "READER-02", "Therapy Room", (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"), "SIMULATION", "Initial scan"),
        (4, "RFID004", "READER-01", "Patient Room", (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"), "SIMULATION", "Initial scan"),
        (5, "RFID005", "READER-03", "Dining Hall", (datetime.now() - timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S"), "SIMULATION", "Initial scan")
    ]
    cursor.executemany("""
        INSERT INTO movement_logs (patient_id, rfid_tag_id, reader_id, location, timestamp, trigger_source, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, logs)

    conn.commit()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    init_db()
