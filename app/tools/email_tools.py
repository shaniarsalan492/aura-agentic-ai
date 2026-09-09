from crewai.tools import tool
from app.services.email_service import send_email


@tool("Send Email Tool")
def send_email_tool(to_address: str, subject: str, body: str) -> str:
    """Sends the final customer email via SMTP.
    Inputs: to_address (customer email), subject, and body (the full email text)."""
    return send_email(to_address, subject, body)