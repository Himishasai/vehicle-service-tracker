<<<<<<< HEAD
CREATE TABLE Owners (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    address TEXT
);

CREATE TABLE Vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER,
    vehicle_number TEXT,
    model TEXT,
    type TEXT
);

CREATE TABLE Mechanics (
    mechanic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    garage_name TEXT
);

CREATE TABLE Services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    mechanic_id INTEGER,
    service_date TEXT,
    description TEXT,
    cost REAL
=======
CREATE TABLE Owners (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    address TEXT
);

CREATE TABLE Vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER,
    vehicle_number TEXT,
    model TEXT,
    type TEXT
);

CREATE TABLE Mechanics (
    mechanic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    garage_name TEXT
);

CREATE TABLE Services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    mechanic_id INTEGER,
    service_date TEXT,
    description TEXT,
    cost REAL
>>>>>>> a1442d9792a99537e7be3135ee40273a833bf3b2
);