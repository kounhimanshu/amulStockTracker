import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

def send_email(subject, body):
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    if not all([smtp_user, smtp_pass, email_from, email_to]):
        print("❌ Environment variables not loaded properly.")
        return

    # Create message
    message = MIMEMultipart()
    message["From"] = email_from
    message["To"] = email_to
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(message)
            print("✅ Test email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# For testing
if __name__ == "__main__":
    send_email(
        subject="📦 Amul Stock Checker Test Mail",
        body="This is a test email from notifier.py via Gmail SMTP."
    )
