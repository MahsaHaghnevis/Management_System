import sqlite3
import random
import string
from datetime import datetime, timedelta

# List of real countries
countries = ["United States", "Canada", "Mexico", "Brazil", "Argentina", "United Kingdom", "France", "Germany", "Italy", "Spain", "China", "Japan", "India", "Russia", "Australia"]
# Predefined lists for order_status and order_type
order_status_list = ["Processing", "Preparation", "In stock", "Sent", "Received", "Returned"]
order_type_list = ["Online", "In person"]

# Connect to SQLite database
conn = sqlite3.connect('warehouse_management.db')
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute('PRAGMA foreign_keys = ON;')

# Drop tables if they exist (for testing purposes)
cursor.execute('DROP TABLE IF EXISTS Country')
cursor.execute('DROP TABLE IF EXISTS TPL')
cursor.execute('DROP TABLE IF EXISTS User')
cursor.execute('DROP TABLE IF EXISTS Warehouse')
cursor.execute('DROP TABLE IF EXISTS Catalog')
cursor.execute('DROP TABLE IF EXISTS Orders')
cursor.execute('DROP TABLE IF EXISTS Location')
cursor.execute('DROP TABLE IF EXISTS OrdersCatalogJoin')

# Create tables
cursor.executescript('''
-- Create Country table
CREATE TABLE Country (
    country_name VARCHAR(50) PRIMARY KEY
);

-- Create TPL table
CREATE TABLE TPL (
    TP_ID NUMERIC PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Create User table
CREATE TABLE User (
    user_ID NUMERIC PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Age NUMERIC NOT NULL,
    Type VARCHAR(10) NOT NULL CHECK (Type IN ('simple', 'admin')),
    TP_ID NUMERIC NOT NULL,
    phone_number VARCHAR(15) NOT NULL CHECK (phone_number GLOB '+[0-9]*'),
    FOREIGN KEY (TP_ID) REFERENCES TPL(TP_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Warehouse table
CREATE TABLE Warehouse (
    warehouse_ID NUMERIC PRIMARY KEY,
    warehouse_name VARCHAR(50) NOT NULL,
    is_open BOOLEAN NOT NULL,
    creation_date TIMESTAMP NOT NULL,
    country VARCHAR(50) NOT NULL,
    TP_ID NUMERIC NOT NULL,
    FOREIGN KEY (TP_ID) REFERENCES TPL(TP_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (country) REFERENCES Country(country_name)
);

-- Create Catalog table
CREATE TABLE Catalog (
    catalog_ID NUMERIC PRIMARY KEY,
    product_type VARCHAR(50) NOT NULL,
    manufacturing_cost NUMERIC NOT NULL,
    selling_price NUMERIC NOT NULL,
    country_origin VARCHAR(50) NOT NULL,
    weight NUMERIC NOT NULL,
    length NUMERIC NOT NULL,
    description VARCHAR(255),
    product_maintenance_ID VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    TP_ID NUMERIC NOT NULL,
    registered_by_user_ID NUMERIC NOT NULL,
    ordered_by_user_ID NUMERIC,
    image BLOB,
    FOREIGN KEY (TP_ID) REFERENCES TPL(TP_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (registered_by_user_ID) REFERENCES User(user_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ordered_by_user_ID) REFERENCES User(user_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (country_origin) REFERENCES Country(country_name),
    CHECK (manufacturing_cost < selling_price)
);

-- Create Orders table
CREATE TABLE Orders (
    order_ID NUMERIC PRIMARY KEY,
    order_date TIMESTAMP NOT NULL,
    Total_cost NUMERIC NOT NULL,
    TP_ID NUMERIC NOT NULL,
    order_user_ID NUMERIC NOT NULL,
    warehouse_ID NUMERIC NOT NULL,
    order_status VARCHAR(50) NOT NULL CHECK (order_status IN ('Processing', 'Preparation', 'In stock', 'Sent', 'Received', 'Returned')),
    order_type VARCHAR(50) NOT NULL CHECK (order_type IN ('Online', 'In person')),
    user_notes VARCHAR(255),
    is_gift BOOLEAN NOT NULL,
    FOREIGN KEY (TP_ID) REFERENCES TPL(TP_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (order_user_ID) REFERENCES User(user_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (warehouse_ID) REFERENCES Warehouse(warehouse_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Location table
CREATE TABLE Location (
    location_ID NUMERIC PRIMARY KEY,
    has_container BOOLEAN NOT NULL,
    TP_ID NUMERIC NOT NULL,
    warehouse_ID NUMERIC NOT NULL,
    notes VARCHAR(255),
    latitude NUMERIC NOT NULL,
    longitude NUMERIC NOT NULL,
    registered_by_user_ID NUMERIC NOT NULL,
    FOREIGN KEY (TP_ID) REFERENCES TPL(TP_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (warehouse_ID) REFERENCES Warehouse(warehouse_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (registered_by_user_ID) REFERENCES User(user_ID) ON DELETE CASCADE ON UPDATE CASCADE
);
''')

# Insert country data
for country in countries:
    cursor.execute('INSERT INTO Country (country_name) VALUES (?)', (country,))

# Function to generate random strings
def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Function to generate random dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

# Function to generate a random phone number
def random_phone():
    return f'+{random.randint(1, 99)}{random.randint(1000000000, 9999999999)}'

# Function to generate product maintenance ID
def generate_unique_product_maintenance_id(product_name, existing_ids):
    while True:
        maintenance_id = f'{product_name[0]}{random.randint(100, 999)}'
        if maintenance_id not in existing_ids:
            return maintenance_id
# Store existing product_maintenance_IDs to ensure uniqueness
existing_product_maintenance_ids = set()

# Set date range for random dates
start_date = datetime(2000, 1, 1)
end_date = datetime(2024, 1, 1)

# Insert data into TPL
for i in range(1, 10001):
    cursor.execute('INSERT INTO TPL (TP_ID, first_name, last_name) VALUES (?, ?, ?)', (i, random_string(5), random_string(7)))

users = []
# Insert data into User
for i in range(1, 10001):
    user_data = (
        i,
        random_string(5),
        random_string(7),
        f'user{i}@example.com',
        random_string(10),
        round(random.uniform(18, 70), 2),
        random.choice(['simple', 'admin']),
        random.randint(1, 10000),
        random_phone()
    )
    users.append(user_data)
    cursor.execute('''
    INSERT INTO User (user_ID, first_name, last_name, Email, Password, Age, Type, TP_ID, phone_number) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', user_data)

# Insert data into Warehouse
for i in range(1, 10001):
    cursor.execute('''
    INSERT INTO Warehouse (warehouse_ID, warehouse_name, is_open, creation_date, country, TP_ID)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        i,
        random_string(10),
        random.choice([True, False]),
        random_date(start_date, end_date),
        random.choice(countries),
        random.randint(1, 10000)
    ))

# Insert data into Catalog
for i in range(1, 10001):
    product_name = random_string(10)
    product_maintenance_id = generate_unique_product_maintenance_id(product_name, existing_product_maintenance_ids)
    existing_product_maintenance_ids.add(product_maintenance_id)
    
    manufacturing_cost = round(random.uniform(10.0, 100.0), 2)
    selling_price = round(random.uniform(manufacturing_cost + 1.0, 200.0), 2)  # Ensure selling_price is always greater than manufacturing_cost

    user = random.choice(users)
    user_id, _, _, _, _, _, _, tp_id, _ = user

    cursor.execute('''
    INSERT INTO Catalog (catalog_ID, product_type, manufacturing_cost, selling_price, country_origin, weight, length, description, product_maintenance_ID, product_name, TP_ID, registered_by_user_ID, ordered_by_user_ID, image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        i,
        random_string(10),
        manufacturing_cost,
        selling_price,
        random.choice(countries),
        round(random.uniform(1.0, 10.0), 2),
        round(random.uniform(1.0, 5.0), 2),
        random.choice([random_string(20), None]),
        product_maintenance_id,
        product_name,
        tp_id,
        random.randint(1, 10000),
        random.choice([user_id, None]),
        random.choice([random_string(10), None])
    ))

# Insert data into Orders
for i in range(1, 10001):
    user = random.choice(users)
    user_id, _, _, _, _, _, _, tp_id, _ = user
    cursor.execute('''
    INSERT INTO Orders (order_ID, order_date, Total_cost, TP_ID, order_user_ID, warehouse_ID, order_status, order_type, user_notes, is_gift)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        i,  # Ensuring order_ID is unique and sequential
        random_date(start_date, end_date),
        round(random.uniform(50.0, 1000.0), 2),
        tp_id,
        user_id,
        random.randint(1, 10000),
        random.choice(order_status_list),  # Ensure order_status is one of the predefined values
        random.choice(order_type_list),    # Ensure order_type is one of the predefined values
        random.choice([random_string(50), None]),
        random.choice([True, False])
    ))

# Insert data into Location
for i in range(1, 10001):
    cursor.execute('''
    INSERT INTO Location (location_ID, has_container, TP_ID, warehouse_ID, notes, latitude, longitude, registered_by_user_ID)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        i,
        random.choice([True, False]),
        random.randint(1, 10000),
        random.randint(1, 10000),
        random.choice([random_string(20), None]),
        round(random.uniform(-90.0, 90.0), 6),
        round(random.uniform(-180.0, 180.0), 6),
        random.randint(1, 10000)
    ))

cursor.execute('''
CREATE TABLE OrdersCatalogJoin (
    order_ID NUMERIC,
    catalog_ID NUMERIC,
    PRIMARY KEY (order_ID, catalog_ID),
    FOREIGN KEY (order_ID) REFERENCES Orders(order_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (catalog_ID) REFERENCES Catalog(catalog_ID) ON DELETE CASCADE ON UPDATE CASCADE
);
''')

# Fetch all order_user_IDs from Orders
cursor.execute('SELECT order_ID, order_user_ID, TP_ID FROM Orders')
orders = cursor.fetchall()

# Fetch all ordered_by_user_IDs from Catalog
cursor.execute('SELECT catalog_ID, ordered_by_user_ID, TP_ID FROM Catalog')
catalogs = cursor.fetchall()

# Check and insert matching data
for order in orders:
    order_id, order_user_id, order_tp_id = order
    for catalog in catalogs:
        catalog_id, ordered_by_user_id, catalog_tp_id = catalog
        if order_user_id == ordered_by_user_id and order_tp_id == catalog_tp_id:
            cursor.execute('''
            INSERT INTO OrdersCatalogJoin (order_ID, catalog_ID)
            VALUES (?, ?)
            ''', (
                order_id,
                catalog_id
            ))

# Commit changes and close connection
conn.commit()
conn.close()

print("Random data inserted successfully!")