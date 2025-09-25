# app/mail.py
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_SERVER=os.getenv("SMTP_HOST"),
    MAIL_PORT=int(os.getenv("SMTP_PORT", "587")),
    MAIL_USERNAME=os.getenv("SMTP_USER"),
    MAIL_PASSWORD=os.getenv("SMTP_PASS"),
    MAIL_FROM=os.getenv("SMTP_FROM") or "noreply@travelmanager.com",
    MAIL_STARTTLS=True,   # 587 → STARTTLS
    MAIL_SSL_TLS=False,   # 不走 465/SSL
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

fm = FastMail(conf)

async def send_verification_email(to_email: str, code: str):
    subject = "Email verification"
    body = f"Your verification code is: {code}"
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype="plain",
    )
    await fm.send_message(message)