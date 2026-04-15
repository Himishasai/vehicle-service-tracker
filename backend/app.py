from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime

app = Flask(__name__, static_folder="../frontend")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = os.path.join(BASE_DIR, "../frontend")

# ---------- DB CONNECTION ----------
def get_db():
    url = os.environ.get("DATABASE_URL")

    # Fix for Render
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return psycopg2.connect(url)

# ---------- INIT DB ----------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Owners (
        owner_id SERIAL PRIMARY KEY,
        name TEXT,
        phone TEXT,
        address TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Vehicles (
        vehicle_id SERIAL PRIMARY KEY,
        owner_id INTEGER REFERENCES Owners(owner_id) ON DELETE CASCADE,
        vehicle_number TEXT,
        model TEXT,
        type TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Services (
        service_id SERIAL PRIMARY KEY,
        vehicle_id INTEGER REFERENCES Vehicles(vehicle_id) ON DELETE CASCADE,
        service_date DATE,
        description TEXT,
        cost REAL
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

# Convert rows to dict
def row_to_dict(cursor, row):
    return {desc[0]: value for desc, value in zip(cursor.description, row)}

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
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO Owners (name, phone, address) VALUES (%s, %s, %s)",
        (data["name"], data["phone"], data["address"])
    )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Owner added"})

@app.route("/get_owners")
def get_owners():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Owners")
    rows = cur.fetchall()

    result = [row_to_dict(cur, r) for r in rows]

    cur.close()
    conn.close()
    return jsonify(result)

@app.route("/delete_owner/<int:id>", methods=["DELETE"])
def delete_owner(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM Owners WHERE owner_id=%s", (id,))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Deleted"})

@app.route("/update_owner/<int:id>", methods=["PUT"])
def update_owner(id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE Owners SET name=%s, phone=%s, address=%s WHERE owner_id=%s",
        (data["name"], data["phone"], data["address"], id)
    )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Updated"})

# ---------- VEHICLE ----------
@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO Vehicles (owner_id, vehicle_number, model, type) VALUES (%s, %s, %s, %s)",
        (data["owner_id"], data["vehicle_number"], data["model"], data["type"])
    )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Vehicle added"})

@app.route("/get_vehicles")
def get_vehicles():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT v.*, o.name as owner_name
        FROM Vehicles v
        JOIN Owners o ON v.owner_id = o.owner_id
    """)

    rows = cur.fetchall()
    result = [row_to_dict(cur, r) for r in rows]

    cur.close()
    conn.close()
    return jsonify(result)

@app.route("/delete_vehicle/<int:id>", methods=["DELETE"])
def delete_vehicle(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM Vehicles WHERE vehicle_id=%s", (id,))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Deleted"})

@app.route("/update_vehicle/<int:id>", methods=["PUT"])
def update_vehicle(id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE Vehicles SET owner_id=%s, vehicle_number=%s, model=%s, type=%s WHERE vehicle_id=%s",
        (data["owner_id"], data["vehicle_number"], data["model"], data["type"], id)
    )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Updated"})

# ---------- SERVICE ----------
@app.route("/add_service", methods=["POST"])
def add_service():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO Services (vehicle_id, service_date, description, cost) VALUES (%s, %s, %s, %s)",
        (data["vehicle_id"], data["service_date"], data["description"], data["cost"])
    )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Service added"})

@app.route("/get_services")
def get_services():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Services")
    rows = cur.fetchall()

    result = [row_to_dict(cur, r) for r in rows]

    cur.close()
    conn.close()
    return jsonify(result)

@app.route("/delete_service/<int:id>", methods=["DELETE"])
def delete_service(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM Services WHERE service_id=%s", (id,))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Deleted"})

@app.route("/update_service/<int:id>", methods=["PUT"])
def update_service(id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE Services SET vehicle_id=%s, service_date=%s, description=%s, cost=%s WHERE service_id=%s",
        (data["vehicle_id"], data["service_date"], data["description"], data["cost"], id)
    )

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Updated"})

# ---------- HISTORY ----------
@app.route("/history")
def history():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.*, v.vehicle_number
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    """)

    rows = cur.fetchall()
    result = [row_to_dict(cur, r) for r in rows]

    cur.close()
    conn.close()
    return jsonify(result)

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Owners")
    owners = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Vehicles")
    vehicles = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Services")
    services = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({"owners": owners, "vehicles": vehicles, "services": services})

# ---------- ALERTS ----------
@app.route("/service_reminders")
def service_reminders():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT v.vehicle_number, s.service_date
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
    """)

    rows = cur.fetchall()

    result = []
    for r in rows:
        days = (datetime.now() - r[1]).days

        status = "OK"
        if days > 180:
            status = "Service Due"
        elif days > 90:
            status = "Upcoming"

        result.append({
            "vehicle": r[0],
            "days": days,
            "status": status
        })

    cur.close()
    conn.close()
    return jsonify(result)

# ---------- RUN ----------
init_db()

if __name__ == "__main__":
    app.run(debug=True)
