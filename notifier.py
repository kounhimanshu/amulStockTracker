import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from email.utils import formataddr


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

load_dotenv(override=True)  # Load .env variables

def send_email(subject, body):
    smtp_user = os.getenv("SMTP_USER")
    logging.info("This is SMTP user: %s",smtp_user)
    smtp_pass = os.getenv("SMTP_PASS")
    # logging.info("This is smtp_pass: %s",smtp_pass)
    email_from = os.getenv("EMAIL_FROM")
    logging.info("This is SMTP email_from: %s",email_from)
    email_from_name = os.getenv("EMAIL_FROM_NAME")
    logging.info("This is SMTP email_from_name: %s",email_from_name)
    email_to = os.getenv("EMAIL_TO")
    logging.info("This is SMTP email_to: %s",email_to)

    if not all([smtp_user, smtp_pass, email_from, email_to]):
        logging.error("Environment variables not loaded properly.")
        return

    message = MIMEMultipart()
    message["From"] = formataddr((email_from_name, email_from))
    message["To"] = email_to
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(message)
            logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# For testing
if __name__ == "__main__":
    send_email(
        subject="Test",
        body="We are testing email service. Sorry for inconvenience"
    )
