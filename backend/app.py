from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/vehicle.db")
FRONTEND = os.path.join(BASE_DIR, "../frontend")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- FRONTEND ----------
@app.route("/")
def home():
    return send_from_directory(FRONTEND, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND, path)

# ---------- ADD ----------
@app.route("/add_owner", methods=["POST"])
def add_owner():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO Owners (name, phone, address) VALUES (?, ?, ?)",
                 (data["name"], data["phone"], data["address"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Owner added"})

@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO Vehicles (owner_id, vehicle_number, model, type) VALUES (?, ?, ?, ?)",
                 (data["owner_id"], data["vehicle_number"], data["model"], data["type"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Vehicle added"})

@app.route("/add_service", methods=["POST"])
def add_service():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO Services (vehicle_id, mechanic_id, service_date, description, cost) VALUES (?, ?, ?, ?, ?)",
                 (data["vehicle_id"], data["mechanic_id"], data["service_date"], data["description"], data["cost"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Service added"})

# ---------- VIEW ----------
@app.route("/service_history")
def history():
    conn = get_db()
    data = conn.execute("""
        SELECT s.service_id, v.vehicle_number, s.service_date, s.description, s.cost
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    """).fetchall()
    conn.close()
    return jsonify([dict(x) for x in data])

# ---------- DELETE ----------
@app.route("/delete_service/<int:id>", methods=["DELETE"])
def delete_service(id):
    conn = get_db()
    conn.execute("DELETE FROM Services WHERE service_id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})

# ---------- UPDATE ----------
@app.route("/update_service/<int:id>", methods=["PUT"])
def update_service(id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE Services SET description=?, cost=? WHERE service_id=?",
                 (data["description"], data["cost"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Updated"})

# ---------- SEARCH ----------
@app.route("/search_vehicle/<v>")
def search(v):
    conn = get_db()
    data = conn.execute("SELECT * FROM Vehicles WHERE vehicle_number LIKE ?", ('%' + v + '%',)).fetchall()
    conn.close()
    return jsonify([dict(x) for x in data])

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    owners = conn.execute("SELECT COUNT(*) FROM Owners").fetchone()[0]
    vehicles = conn.execute("SELECT COUNT(*) FROM Vehicles").fetchone()[0]
    services = conn.execute("SELECT COUNT(*) FROM Services").fetchone()[0]
    conn.close()

    return jsonify({
        "owners": owners,
        "vehicles": vehicles,
        "services": services
    })

if __name__ == "__main__":
    app.run(port=10000, debug=True)
