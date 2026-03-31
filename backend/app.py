from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="../frontend")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/vehicle.db")
FRONTEND_FOLDER = os.path.join(BASE_DIR, "../frontend")

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- SERVE UI ----------------
@app.route("/")
def serve_ui():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/<path:path>")
def serve_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# ---------------- ADD OWNER ----------------
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

# ---------------- ADD VEHICLE ----------------
@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Vehicles (owner_id, vehicle_number, model, type) VALUES (?, ?, ?, ?)",
        (data["owner_id"], data["vehicle_number"], data["model"], data["type"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Vehicle added successfully"})

# ---------------- ADD SERVICE ----------------
@app.route("/add_service", methods=["POST"])
def add_service():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Services (vehicle_id, service_date, description, cost, mechanic_id) VALUES (?, ?, ?, ?, ?)",
        (data["vehicle_id"], data["service_date"], data["description"], data["cost"], data["mechanic_id"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Service added successfully"})

# ---------------- HISTORY ----------------
@app.route("/service_history", methods=["GET"])
def service_history():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.vehicle_number, s.service_date, s.description, s.cost
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Owners")
    owners = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Vehicles")
    vehicles = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Services")
    services = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "owners": owners,
        "vehicles": vehicles,
        "services": services
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
