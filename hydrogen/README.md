# CareSync - Smart Patient Monitoring System

CareSync is an AI-enabled smart patient monitoring & RFID tracking system built for hospitals, assisted-living facilities, and memory care units.

## Features
- **Live Dashboard**: Real-time zone occupancy, recent scans, and active alerts.
- **Facility Map**: Live SVG floor plan showing patient locations in real-time.
- **Alert System**: Automated alerts (e.g., restricted zone entry by a wandering-risk patient).
- **RFID Integration**: REST API endpoint for physical ESP32/RC522 hardware, plus a web simulator.

## Setup & Running Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database** (this creates `caresync.db` and populates it with dummy data):
   ```bash
   python database/seed_data.py
   ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open a browser and navigate to `http://localhost:5000`

## Demo Credentials
- **Admin**: `admin` / `admin123`
- **Caregiver**: `caregiver` / `caregiver123`

## API Details
The core endpoint for hardware integration is:
`POST /api/rfid/scan`
Payload:
```json
{
  "tag_id": "RFID001",
  "reader_id": "READER-01",
  "trigger_source": "HARDWARE"
}
```
