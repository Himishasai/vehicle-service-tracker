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
    type TEXT,
    FOREIGN KEY (owner_id) REFERENCES Owners(owner_id) ON DELETE CASCADE
);

CREATE TABLE Services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    service_date TEXT,
    description TEXT,
    cost REAL,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE CASCADE
);
