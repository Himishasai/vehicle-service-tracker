<<<<<<< HEAD
import sqlite3

conn = sqlite3.connect("../database/vehicle.db")

with open("../database/schema.sql", "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

=======
import sqlite3

conn = sqlite3.connect("../database/vehicle.db")

with open("../database/schema.sql", "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

>>>>>>> a1442d9792a99537e7be3135ee40273a833bf3b2
print("Database created!")