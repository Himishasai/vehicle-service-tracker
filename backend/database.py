<<<<<<< HEAD
import sqlite3

def get_db():
    conn = sqlite3.connect("../database/vehicle.db")
    conn.row_factory = sqlite3.Row
=======
import sqlite3

def get_db():
    conn = sqlite3.connect("../database/vehicle.db")
    conn.row_factory = sqlite3.Row
>>>>>>> a1442d9792a99537e7be3135ee40273a833bf3b2
    return conn