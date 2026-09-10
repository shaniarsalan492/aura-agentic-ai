"""Tests for the database layer: connection, schema, and referential integrity."""

from app.database.db import get_connection


def test_connection_works():
    conn = get_connection()
    assert conn is not None
    conn.close()


def test_orders_table_has_expected_columns():
    conn = get_connection()
    cursor = conn.execute("PRAGMA table_info(orders)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    expected = ["order_id", "customer_id", "product_name", "quantity",
                "price", "order_status", "delivery_status", "order_date"]
    for col in expected:
        assert col in columns


def test_orders_have_valid_customer_references():
    """Every order.customer_id should exist in the customers table (referential integrity)."""
    conn = get_connection()
    orphans = conn.execute("""
        SELECT o.order_id FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """).fetchall()
    conn.close()
    assert len(orphans) == 0, f"Found orders with no matching customer: {orphans}"


def test_sample_order_exists():
    conn = get_connection()
    row = conn.execute("SELECT * FROM orders WHERE order_id = 'ORD1052'").fetchone()
    conn.close()
    assert row is not None