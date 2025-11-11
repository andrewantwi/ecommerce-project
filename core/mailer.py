import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from dotenv import load_dotenv

load_dotenv()

base_url=os.getenv("BASE_URL")
gmail_address = os.getenv("GMAIL_ADDRESS")
gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")


def send_reset_email(email: str, reset_link: str):
    sender_email = gmail_address
    sender_password = gmail_app_password
    subject = "Password Reset Request"

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject

    text = f"Hi,\n\nTo reset your password, click the link below:\n{reset_link}\n\nThis link expires in 15 minutes."
    html = f"""
    <html>
        <body>
            <p>Hi,<br><br>
            Click the link below to reset your password:<br>
            <a href="{reset_link}">Reset Password</a><br><br>
            This link expires in 15 minutes.
            </p>
        </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())

    print(f"[INFO] Password reset email sent to {email}")

def send_verification_email(email: str, token: str):
    verify_link = f"{base_url}/auth/verify?token={token}"
    msg = MIMEText(f"Click this link to verify your email: {verify_link}")
    msg['Subject'] = 'Verify your email'
    msg['From'] = 'no-reply@yourapp.com'
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "app_password")
        server.send_message(msg)
