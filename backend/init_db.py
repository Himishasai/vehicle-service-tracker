import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/vehicle.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ---------------- CREATE TABLES ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS Owners (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    address TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER,
    vehicle_number TEXT,
    model TEXT,
    type TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Mechanics (
    mechanic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    garage_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    mechanic_id INTEGER,
    service_date TEXT,
    description TEXT,
    cost REAL
)
""")

# ---------------- SAMPLE DATA ----------------

# Owner
cursor.execute("""
INSERT INTO Owners (name, phone, address)
VALUES ('Rahul', '9876543210', 'Chennai')
""")

# Vehicle
cursor.execute("""
INSERT INTO Vehicles (owner_id, vehicle_number, model, type)
VALUES (1, 'TN01AB1234', 'Honda Activa', 'Bike')
""")

# Mechanic
cursor.execute("""
INSERT INTO Mechanics (name, phone, garage_name)
VALUES ('Kumar', '9123456780', 'Kumar Garage')
""")

# Service
cursor.execute("""
INSERT INTO Services (vehicle_id, mechanic_id, service_date, description, cost)
VALUES (1, 1, '2026-04-01', 'Oil Change', 500)
""")

conn.commit()
conn.close()

print("Database created with sample data ✅")
