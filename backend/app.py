from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="../frontend")
CORS(app)

# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    conn = sqlite3.connect("database/vehicle.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "Backend Running 🚀"


# =========================
# SERVE FRONTEND
# =========================
@app.route("/ui")
def ui():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    if data["username"] == "admin" and data["password"] == "1234":
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"})


# =========================
# ADD OWNER
# =========================
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


# =========================
# ADD VEHICLE
# =========================
@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Vehicles (vehicle_number, model, owner_id) VALUES (?, ?, ?)",
        (data["vehicle_number"], data["model"], data["owner_id"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Vehicle added successfully"})


# =========================
# ADD SERVICE
# =========================
@app.route("/add_service", methods=["POST"])
def add_service():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO Services 
        (vehicle_id, service_date, description, cost, mechanic_id) 
        VALUES (?, ?, ?, ?, ?)""",
        (
            data["vehicle_id"],
            data["service_date"],
            data["description"],
            data["cost"],
            data["mechanic_id"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Service added successfully"})


# =========================
# VIEW HISTORY
# =========================
@app.route("/service_history", methods=["GET"])
def service_history():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.vehicle_number,
               s.service_date,
               s.description,
               s.cost,
               m.name as mechanic_name
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
        JOIN Mechanics m ON s.mechanic_id = m.mechanic_id
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


# =========================
# DASHBOARD STATS
# =========================
@app.route("/stats")
def stats():
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


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
