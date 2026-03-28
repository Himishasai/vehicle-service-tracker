from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("../database/vehicle.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Backend Running 🚀"

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
    return jsonify({"message": "Owner added"})

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
    return jsonify({"message": "Vehicle added"})

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
    return jsonify({"message": "Service added"})

# ---------------- VIEW HISTORY ----------------
@app.route("/service_history", methods=["GET"])
def service_history():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.vehicle_number, s.service_date, s.description, s.cost, m.name AS mechanic
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
        JOIN Mechanics m ON s.mechanic_id = m.mechanic_id
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)