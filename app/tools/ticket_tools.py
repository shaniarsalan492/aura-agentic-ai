from crewai.tools import tool
from app.database.db import get_connection


@tool("Create Support Ticket Tool")
def create_ticket_tool(order_id: str, customer_id: str, sentiment: str, priority: str, summary: str) -> str:
    """Creates a support ticket for tracking/escalation.
    Inputs: order_id, customer_id, sentiment (positive/neutral/negative/angry),
    priority (low/medium/high/urgent), and a short summary of the issue."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tickets (order_id, customer_id, sentiment, priority, summary, status) "
        "VALUES (?, ?, ?, ?, ?, 'open')",
        (order_id.strip(), customer_id.strip(), sentiment.strip(), priority.strip(), summary.strip())
    )
    conn.commit()
    conn.close()
    return f"Ticket created for order {order_id} — sentiment: {sentiment}, priority: {priority}."