CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS rfid_readers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reader_id TEXT UNIQUE NOT NULL,
    location_name TEXT NOT NULL,
    is_restricted INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Active',
    description TEXT
);

CREATE TABLE IF NOT EXISTS rfid_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id TEXT UNIQUE NOT NULL,
    tag_label TEXT,
    status TEXT NOT NULL DEFAULT 'Available',
    assigned_patient_id INTEGER,
    FOREIGN KEY(assigned_patient_id) REFERENCES patients(id)
);

CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    medical_condition TEXT,
    rfid_tag_id TEXT,
    assigned_caregiver_id INTEGER,
    current_location TEXT,
    room_number TEXT,
    status TEXT NOT NULL DEFAULT 'Normal',
    emergency_contact TEXT,
    notes TEXT,
    last_seen DATETIME,
    FOREIGN KEY(rfid_tag_id) REFERENCES rfid_tags(tag_id),
    FOREIGN KEY(assigned_caregiver_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS movement_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    rfid_tag_id TEXT,
    reader_id TEXT,
    location TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    trigger_source TEXT,
    notes TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_code TEXT UNIQUE NOT NULL,
    patient_id INTEGER,
    alert_type TEXT NOT NULL,
    location TEXT,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Active',
    acknowledged_by INTEGER,
    resolved_by INTEGER,
    resolution_notes TEXT,
    resolved_at DATETIME,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(acknowledged_by) REFERENCES users(id),
    FOREIGN KEY(resolved_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS activity_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    activity_name TEXT NOT NULL,
    expected_location TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    days_of_week TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);
