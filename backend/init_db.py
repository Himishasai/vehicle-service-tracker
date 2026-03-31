import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/vehicle.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables
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

conn.commit()
conn.close()

print("Database created successfully ✅")
