from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="../frontend")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ FIXED DB PATH (IMPORTANT FOR RENDER)
DB_PATH = os.path.join(BASE_DIR, "vehicle.db")

FRONTEND_FOLDER = os.path.join(BASE_DIR, "../frontend")

# ---------- DB ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ✅ CREATE TABLES IF NOT EXIST (VERY IMPORTANT FOR RENDER)
def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Owners (
        owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        address TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Vehicles (
        vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        vehicle_number TEXT,
        model TEXT,
        type TEXT,
        FOREIGN KEY(owner_id) REFERENCES Owners(owner_id) ON DELETE CASCADE
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Services (
        service_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER,
        service_date TEXT,
        description TEXT,
        cost REAL,
        FOREIGN KEY(vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

# ---------- ROUTES ----------
@app.route("/")
def home():
    return "Backend Running 🚀"

@app.route("/ui")
def ui():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/login.html")
def login():
    return send_from_directory(FRONTEND_FOLDER, "login.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# ---------- OWNER ----------
@app.route("/add_owner", methods=["POST"])
def add_owner():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO Owners (name, phone, address) VALUES (?, ?, ?)",
        (data["name"], data["phone"], data["address"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Owner added"})

@app.route("/get_owners")
def get_owners():
    conn = get_db()
    rows = conn.execute("SELECT * FROM Owners").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/delete_owner/<int:id>", methods=["DELETE"])
def delete_owner(id):
    conn = get_db()

    conn.execute("""
        DELETE FROM Services
        WHERE vehicle_id IN (
            SELECT vehicle_id FROM Vehicles WHERE owner_id=?
        )
    """, (id,))

    conn.execute("DELETE FROM Vehicles WHERE owner_id=?", (id,))
    conn.execute("DELETE FROM Owners WHERE owner_id=?", (id,))

    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})

@app.route("/update_owner/<int:id>", methods=["PUT"])
def update_owner(id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE Owners SET name=?, phone=?, address=? WHERE owner_id=?",
        (data["name"], data["phone"], data["address"], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Updated"})

# ---------- VEHICLE ----------
@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO Vehicles (owner_id, vehicle_number, model, type) VALUES (?, ?, ?, ?)",
        (data["owner_id"], data["vehicle_number"], data["model"], data["type"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Vehicle added"})

@app.route("/get_vehicles")
def get_vehicles():
    conn = get_db()
    rows = conn.execute("""
        SELECT v.*, o.name as owner_name
        FROM Vehicles v
        JOIN Owners o ON v.owner_id = o.owner_id
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/delete_vehicle/<int:id>", methods=["DELETE"])
def delete_vehicle(id):
    conn = get_db()
    conn.execute("DELETE FROM Services WHERE vehicle_id=?", (id,))
    conn.execute("DELETE FROM Vehicles WHERE vehicle_id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})

@app.route("/update_vehicle/<int:id>", methods=["PUT"])
def update_vehicle(id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE Vehicles SET owner_id=?, vehicle_number=?, model=?, type=? WHERE vehicle_id=?",
        (data["owner_id"], data["vehicle_number"], data["model"], data["type"], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Updated"})

# ---------- SERVICE ----------
@app.route("/add_service", methods=["POST"])
def add_service():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO Services (vehicle_id, service_date, description, cost) VALUES (?, ?, ?, ?)",
        (data["vehicle_id"], data["service_date"], data["description"], data["cost"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Service added"})

@app.route("/get_services")
def get_services():
    conn = get_db()
    rows = conn.execute("SELECT * FROM Services").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/delete_service/<int:id>", methods=["DELETE"])
def delete_service(id):
    conn = get_db()
    conn.execute("DELETE FROM Services WHERE service_id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})

@app.route("/update_service/<int:id>", methods=["PUT"])
def update_service(id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE Services SET vehicle_id=?, service_date=?, description=?, cost=? WHERE service_id=?",
        (data["vehicle_id"], data["service_date"], data["description"], data["cost"], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Updated"})

# ---------- HISTORY ----------
@app.route("/history")
def history():
    conn = get_db()
    rows = conn.execute("""
        SELECT s.*, v.vehicle_number
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    owners = conn.execute("SELECT COUNT(*) FROM Owners").fetchone()[0]
    vehicles = conn.execute("SELECT COUNT(*) FROM Vehicles").fetchone()[0]
    services = conn.execute("SELECT COUNT(*) FROM Services").fetchone()[0]
    conn.close()
    return jsonify({"owners": owners, "vehicles": vehicles, "services": services})

# ---------- ALERTS (YOU WERE MISSING THIS 🔥) ----------
@app.route("/service_reminders")
def service_reminders():
    conn = get_db()
    rows = conn.execute("""
        SELECT v.vehicle_number, s.service_date
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    """).fetchall()

    from datetime import datetime

    result = []
    for r in rows:
        days = (datetime.now() - datetime.strptime(r["service_date"], "%Y-%m-%d")).days

        status = "OK"
        if days > 180:
            status = "Service Due"
        elif days > 90:
            status = "Upcoming"

        result.append({
            "vehicle": r["vehicle_number"],
            "days": days,
            "status": status
        })

    conn.close()
    return jsonify(result)

# ---------- RUN ----------
if __name__ == "__main__":
    init_db()   # ✅ ensures DB exists in Render
    app.run(debug=True)
