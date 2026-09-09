import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.settings import SMTP_EMAIL, SMTP_APP_PASSWORD


def send_email(to_address: str, subject: str, body: str) -> str:
    """Sends an email via Gmail SMTP. Returns a status message."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_address, msg.as_string())

        return f"Email sent successfully to {to_address}."
    except Exception as e:
        return f"Failed to send email: {e}"