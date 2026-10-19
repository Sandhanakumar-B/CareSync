import os
from flask import Flask, redirect, url_for
from database import db
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.patient_routes import patient_bp
from routes.rfid_routes import rfid_bp
from routes.map_routes import map_bp
from routes.alert_routes import alert_bp
from routes.log_routes import log_bp
from routes.api_routes import api_bp

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_caresync'

# Initialize database teardown
db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(rfid_bp)
app.register_blueprint(map_bp)
app.register_blueprint(alert_bp)
app.register_blueprint(log_bp)
app.register_blueprint(api_bp)

@app.route('/')
def index():
    return redirect(url_for('dashboard.index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
