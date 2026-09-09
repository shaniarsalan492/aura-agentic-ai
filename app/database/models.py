import sqlite3
from app.config.settings import DB_PATH


def create_database():
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sample_customers = [
        ("CUST001", "Ali Khan", "ali.khan@example.com", "+92-300-1234567"),
        ("CUST002", "Sara Ahmed", "sara.ahmed@example.com", "+92-301-2345678"),
        ("CUST003", "Bilal Raza", "bilal.raza@example.com", "+92-302-3456789"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO customers (customer_id, customer_name, email, phone) VALUES (?, ?, ?, ?)",
        sample_customers
    )

    sample_orders = [
        ("ORD1052", "CUST001", "Wireless Headphones", 1, 45.00, "Processing", "Delayed", "2026-08-25"),
        ("ORD1053", "CUST002", "Laptop Stand", 2, 80.00, "Delivered", "Delivered", "2026-08-20"),
        ("ORD1054", "CUST003", "Smart Watch", 1, 120.00, "Shipped", "In Transit", "2026-09-01"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO orders (order_id, customer_id, product_name, quantity, price, order_status, delivery_status, order_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        sample_orders
    )

    conn.commit()
    conn.close()
    print("Sample data inserted.")


if __name__ == "__main__":
    create_database()
    seed_sample_data()