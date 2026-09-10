from crewai.tools import tool
from app.database.db import get_connection
from app.utils.logger import get_logger
from app.models.schemas import OrderSchema

logger = get_logger(__name__)


@tool("Order Lookup Tool")
def order_lookup_tool(order_id: str) -> str:
    """Looks up an order by its order ID in the business database.
    Input should be an order ID like 'ORD1052'."""
    logger.info(f"Looking up order: {order_id}")
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
        logger.warning(f"Order not found: {order_id}")
        return f"No order found with ID {order_id}."

    order = OrderSchema(
        order_id=row[0],
        customer_id="",  # not selected in this query; fine to leave blank here
        customer_name=row[1],
        customer_email=row[2],
        product_name=row[3],
        quantity=row[4],
        price=row[5],
        order_status=row[6],
        delivery_status=row[7],
        order_date=row[8],
    )
    logger.info(f"Order found: {order_id}")
    return order.model_dump_json()