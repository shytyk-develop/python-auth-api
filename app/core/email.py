"""Email utility for sending emails via SMTP."""
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    body: str,
    body_html: str | None = None,
) -> bool:
    """Send email via SMTP. Returns False if SMTP not configured."""
    if not settings.smtp_user or not settings.smtp_password:
        logger.warning("SMTP not configured - email to %s: %s", to_email, subject)
        return False
    
    try:
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        text_part = MIMEText(body, "plain")
        message.attach(text_part)
        
        if body_html:
            html_part = MIMEText(body_html, "html")
            message.attach(html_part)
        
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            start_tls=True,
        )
        logger.info("Email sent to %s", to_email)
        return True
    except Exception as e:
        logger.error("Failed to send to %s: %s", to_email, str(e))
        return False
