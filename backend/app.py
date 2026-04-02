from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_PATH = os.path.join(BASE_DIR, "../frontend")

app = Flask(__name__, static_folder=FRONTEND_PATH)

DB_PATH = os.path.join(BASE_DIR, "../database/vehicle.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- ROUTES ----------
@app.route("/")
def login_page():
    return send_from_directory(FRONTEND_PATH, "login.html")

@app.route("/ui")
def ui():
    return send_from_directory(FRONTEND_PATH, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_PATH, path)

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data.get("username") == "admin" and data.get("password") == "1234":
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"})

# ---------- OWNER ----------
@app.route("/add_owner", methods=["POST"])
def add_owner():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO Owners (name, phone, address) VALUES (?, ?, ?)",
                 (data["name"], data["phone"], data["address"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Owner added"})

@app.route("/get_owners")
def get_owners():
    conn = get_db()
    data = conn.execute("SELECT * FROM Owners").fetchall()
    conn.close()
    return jsonify([dict(x) for x in data])

@app.route("/update_owner/<int:id>", methods=["PUT"])
def update_owner(id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE Owners SET name=?, phone=?, address=? WHERE owner_id=?",
                 (data["name"], data["phone"], data["address"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Owner Updated"})

@app.route("/delete_owner/<int:id>", methods=["DELETE"])
def delete_owner(id):
    conn = get_db()
    conn.execute("DELETE FROM Owners WHERE owner_id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})

# ---------- VEHICLE ----------
@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO Vehicles (owner_id, vehicle_number, model, type) VALUES (?, ?, ?, ?)",
                 (data["owner_id"], data["vehicle_number"], data["model"], data["type"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Vehicle added"})

@app.route("/get_vehicles")
def get_vehicles():
    conn = get_db()
    data = conn.execute("SELECT * FROM Vehicles").fetchall()
    conn.close()
    return jsonify([dict(x) for x in data])

@app.route("/update_vehicle/<int:id>", methods=["PUT"])
def update_vehicle(id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE Vehicles SET owner_id=?, vehicle_number=?, model=?, type=? WHERE vehicle_id=?",
                 (data["owner_id"], data["vehicle_number"], data["model"], data["type"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Vehicle Updated"})

@app.route("/delete_vehicle/<int:id>", methods=["DELETE"])
def delete_vehicle(id):
    conn = get_db()
    conn.execute("DELETE FROM Vehicles WHERE vehicle_id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Vehicle Deleted"})

# ---------- SERVICE ----------
@app.route("/add_service", methods=["POST"])
def add_service():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO Services (vehicle_id, service_date, description, cost) VALUES (?, ?, ?, ?)",
                 (data["vehicle_id"], data["service_date"], data["description"], data["cost"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Service added"})

@app.route("/get_services")
def get_services():
    conn = get_db()
    data = conn.execute("SELECT * FROM Services").fetchall()
    conn.close()
    return jsonify([dict(x) for x in data])

@app.route("/update_service/<int:id>", methods=["PUT"])
def update_service(id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE Services SET vehicle_id=?, service_date=?, description=?, cost=? WHERE service_id=?",
                 (data["vehicle_id"], data["service_date"], data["description"], data["cost"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Service Updated"})

@app.route("/delete_service/<int:id>", methods=["DELETE"])
def delete_service(id):
    conn = get_db()
    conn.execute("DELETE FROM Services WHERE service_id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Service Deleted"})

# ---------- HISTORY ----------
@app.route("/history")
def history():
    conn = get_db()
    data = conn.execute("""
        SELECT s.service_id, v.vehicle_number, s.service_date, s.description, s.cost
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    """).fetchall()
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
    return jsonify({"owners": owners, "vehicles": vehicles, "services": services})

if __name__ == "__main__":
    app.run(debug=True)
