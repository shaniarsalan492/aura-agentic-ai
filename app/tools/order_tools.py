from crewai.tools import tool
from app.database.db import get_connection


@tool("Order Lookup Tool")
def order_lookup_tool(order_id: str) -> str:
    """Looks up an order by its order ID in the business database.
    Input should be an order ID like 'ORD1052'."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.order_id, c.customer_name, c.email, o.product_name, o.quantity,
               o.price, o.order_status, o.delivery_status, o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_id = ?
    """, (order_id.strip(),))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return f"No order found with ID {order_id}."

    columns = ["order_id", "customer_name", "customer_email", "product_name",
               "quantity", "price", "order_status", "delivery_status", "order_date"]
    return str(dict(zip(columns, row)))