from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend Running"

# ADD OWNER
@app.route("/add_owner", methods=["POST"])
def add_owner():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Owners (name, phone, address) VALUES (?, ?, ?)",
                   (data['name'], data['phone'], data['address']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Owner added"})

# ADD VEHICLE
@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Vehicles (owner_id, vehicle_number, model, type) VALUES (?, ?, ?, ?)",
                   (data['owner_id'], data['vehicle_number'], data['model'], data['type']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Vehicle added"})

# ADD MECHANIC
@app.route("/add_mechanic", methods=["POST"])
def add_mechanic():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Mechanics (name, phone, garage_name) VALUES (?, ?, ?)",
                   (data['name'], data['phone'], data['garage_name']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mechanic added"})

# ADD SERVICE
@app.route("/add_service", methods=["POST"])
def add_service():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Services (vehicle_id, mechanic_id, service_date, description, cost) VALUES (?, ?, ?, ?, ?)",
                   (data['vehicle_id'], data['mechanic_id'], data['service_date'], data['description'], data['cost']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Service added"})

# VIEW HISTORY
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

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=10000)