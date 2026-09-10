from crewai.tools import tool
from app.services.email_service import send_email
from app.utils.logger import get_logger

logger = get_logger(__name__)


@tool("Send Email Tool")
def send_email_tool(to_address: str, subject: str, body: str) -> str:
    """Sends the final customer email via SMTP.
    Inputs: to_address (customer email), subject, and body (the full email text)."""
    logger.info(f"Sending email to {to_address} | subject: {subject}")
    result = send_email(to_address, subject, body)
    if "successfully" in result.lower():
        logger.info(f"Email sent successfully to {to_address}")
    else:
        logger.error(f"Email send failed for {to_address}: {result}")
    return result