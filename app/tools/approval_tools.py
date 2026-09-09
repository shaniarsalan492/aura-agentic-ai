from crewai.tools import tool
from app.database.db import get_connection


@tool("Approval Request Tool")
def create_approval_request(order_id: str, request_type: str) -> str:
    """Creates a pending human approval request for a sensitive action (e.g. a refund $50+).
    Input: order_id (e.g. 'ORD1052') and request_type (e.g. 'refund')."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO approvals (order_id, request_type, status) VALUES (?, ?, 'pending')",
        (order_id.strip(), request_type.strip())
    )
    conn.commit()
    conn.close()
    return f"Approval request created for order {order_id} ({request_type})."