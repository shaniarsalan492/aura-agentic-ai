import os
import sqlite3
from app.config.settings import DB_PATH


def create_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        customer_name TEXT NOT NULL,
        email TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL,
        order_status TEXT NOT NULL,
        delivery_status TEXT NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS approvals (
        approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        request_type TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        customer_id TEXT,
        sentiment TEXT,
        priority TEXT,
        summary TEXT,
        status TEXT DEFAULT 'open',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

def seed_sample_data():
    import random

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    first_names = ["Ali", "Sara", "Bilal", "Ayesha", "Hamza", "Zara", "Omar", "Fatima",
                   "Usman", "Mariam", "Ahmed", "Noor", "Tariq", "Hina", "Saad", "Amna",
                   "Kashif", "Sana", "Imran", "Laiba"]
    last_names = ["Khan", "Ahmed", "Raza", "Siddiqui", "Malik", "Hussain", "Iqbal",
                  "Farooq", "Sheikh", "Butt", "Qureshi", "Chaudhry", "Baig", "Rizvi"]

    products = [
        ("Wireless Headphones", 45.00), ("Laptop Stand", 40.00), ("Smart Watch", 120.00),
        ("Bluetooth Speaker", 35.00), ("USB-C Hub", 28.00), ("Mechanical Keyboard", 75.00),
        ("Wireless Mouse", 22.00), ("Webcam HD", 55.00), ("Phone Case", 15.00),
        ("Portable Charger", 30.00), ("Noise Cancelling Earbuds", 89.00), ("Tablet Stand", 25.00),
        ("Gaming Headset", 65.00), ("External SSD 1TB", 95.00), ("Ring Light", 32.00),
        ("Monitor Arm", 48.00), ("Desk Lamp", 20.00), ("Cable Organizer", 12.00),
        ("Smart Plug", 18.00), ("Fitness Tracker", 55.00),
    ]

    order_statuses = ["Processing", "Shipped", "Delivered", "Delayed"]
    delivery_statuses = ["Delayed", "In Transit", "Delivered"]

    sample_customers = [
        ("CUST001", "Ali Khan", "ali.khan@example.com", "+92-300-1234567"),
        ("CUST002", "Sara Ahmed", "sara.ahmed@example.com", "+92-301-2345678"),
        ("CUST003", "Bilal Raza", "bilal.raza@example.com", "+92-302-3456789"),
    ]

    # Generate 47 more customers (CUST004 - CUST050)
    for i in range(4, 51):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        cust_id = f"CUST{i:03d}"
        email = f"{fname.lower()}.{lname.lower()}{i}@example.com"
        phone = f"+92-3{random.randint(0,9)}{random.randint(0,9)}-{random.randint(1000000,9999999)}"
        sample_customers.append((cust_id, f"{fname} {lname}", email, phone))

    cursor.executemany(
        "INSERT OR IGNORE INTO customers (customer_id, customer_name, email, phone) VALUES (?, ?, ?, ?)",
        sample_customers
    )

    sample_orders = [
        ("ORD1052", "CUST001", "Wireless Headphones", 1, 45.00, "Processing", "Delayed", "2026-08-25"),
        ("ORD1053", "CUST002", "Laptop Stand", 2, 80.00, "Delivered", "Delivered", "2026-08-20"),
        ("ORD1054", "CUST003", "Smart Watch", 1, 120.00, "Shipped", "In Transit", "2026-09-01"),
    ]

    # Generate 97 more orders (ORD1055 - ORD1151)
    for i in range(1055, 1152):
        cust = random.choice(sample_customers)
        product_name, base_price = random.choice(products)
        qty = random.randint(1, 3)
        price = round(base_price * qty, 2)
        o_status = random.choice(order_statuses)
        d_status = random.choice(delivery_statuses)
        day_offset = random.randint(1, 30)
        order_date = f"2026-{random.randint(7,9):02d}-{day_offset:02d}"

        sample_orders.append((
            f"ORD{i}", cust[0], product_name, qty, price, o_status, d_status, order_date
        ))

    cursor.executemany(
        "INSERT OR IGNORE INTO orders (order_id, customer_id, product_name, quantity, price, order_status, delivery_status, order_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        sample_orders
    )

    conn.commit()
    conn.close()
    print(f"Sample data inserted: {len(sample_customers)} customers, {len(sample_orders)} orders.")

if __name__ == "__main__":
    create_database()
    seed_sample_data()