from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# DATABASE
def get_db():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "../database/vehicle.db"))
    conn.row_factory = sqlite3.Row
    return conn

# ========================
# UI ROUTES
# ========================

@app.route("/")
def home():
    return "Vehicle Service API Running 🚀"

@app.route("/ui")
def serve_ui():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/ui/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

# ========================
# API ROUTES
# ========================

# ADD OWNER
@app.route("/add_owner", methods=["POST"])
def add_owner():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Owners (name, phone, address) VALUES (?, ?, ?)",
        (data["name"], data["phone"], data["address"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Owner added successfully"})

# GET OWNERS
@app.route("/owners", methods=["GET"])
def get_owners():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Owners")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# ADD VEHICLE
@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Vehicles (owner_id, vehicle_number, model) VALUES (?, ?, ?)",
        (data["owner_id"], data["vehicle_number"], data["model"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Vehicle added successfully"})

# GET VEHICLES
@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vehicles")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# ADD SERVICE
@app.route("/add_service", methods=["POST"])
def add_service():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Services (vehicle_id, description, service_date, mechanic_name) VALUES (?, ?, ?, ?)",
        (data["vehicle_id"], data["description"], data["service_date"], data["mechanic_name"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Service added successfully"})

# VIEW HISTORY
@app.route("/service_history", methods=["GET"])
def service_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.vehicle_number, s.description, s.service_date, s.mechanic_name
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    """)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(debug=True)
