from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="../frontend")
CORS(app)

# PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/vehicle.db")
FRONTEND_FOLDER = os.path.join(BASE_DIR, "../frontend")

# DATABASE
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# HOME
@app.route("/")
def home():
    return "Backend Running 🚀"

# SERVE UI
@app.route("/ui")
def ui():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# ---------------- OWNER CRUD ----------------

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

    return jsonify({"message": "Owner added"})

# GET OWNERS
@app.route("/get_owners", methods=["GET"])
def get_owners():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Owners")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])

# DELETE OWNER
@app.route("/delete_owner/<int:id>", methods=["DELETE"])
def delete_owner(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Owners WHERE owner_id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})

# UPDATE OWNER
@app.route("/update_owner/<int:id>", methods=["PUT"])
def update_owner(id):
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Owners
        SET name=?, phone=?, address=?
        WHERE owner_id=?
    """, (data["name"], data["phone"], data["address"], id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})

# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET"])
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Vehicles")
    v = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Services")
    s = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(cost) FROM Services")
    c = cursor.fetchone()[0] or 0

    conn.close()

    return jsonify({
        "total_vehicles": v,
        "total_services": s,
        "total_cost": c
    })

# ---------------- HISTORY ----------------
@app.route("/service_history", methods=["GET"])
def history():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            v.vehicle_number,
            s.service_date,
            s.description,
            s.cost,
            m.name AS mechanic
        FROM Services s
        JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
        JOIN Mechanics m ON s.mechanic_id = m.mechanic_id
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])

# RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
