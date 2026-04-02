import sqlite3

conn = sqlite3.connect("../database/vehicle.db")
cur = conn.cursor()

with open("../database/schema.sql") as f:
    cur.executescript(f.read())

conn.commit()
conn.close()

print("Database created ✅")
