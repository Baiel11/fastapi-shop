"""Email delivery for auth flows.

Transport: Gmail SMTP with an App Password (requires 2FA on the account).
Credentials live in .env via Settings — never hardcoded here.

If SMTP credentials are missing (fresh clone, colleague without .env),
sending degrades to a log message instead of crashing the request.
"""
import asyncio
import logging
import smtplib
from email.message import EmailMessage

from ...core.config import settings

logger = logging.getLogger("app.mailer")


async def send_password_reset_email(to_email: str, reset_link: str) -> None:
    subject = "Reset your password"
    body = (
        f"We received a request to reset your password.\n\n"
        f"Open this link to choose a new one "
        f"(valid for {settings.reset_token_expire_minutes} minutes):\n"
        f"{reset_link}\n\n"
        f"If you didn't request this, you can safely ignore this email."
    )

    if not settings.smtp_configured:
        logger.warning(
            "SMTP not configured (SMTP_USER/SMTP_PASSWORD missing) — "
            "printing email instead of sending it."
        )
        _log_email(to_email, subject, body)
        return

    msg = EmailMessage()
    msg["From"] = settings.email_from or settings.smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # smtplib is blocking I/O — run it on a worker thread so the event loop
    # (and therefore every other request) stays responsive while Gmail talks.
    await asyncio.to_thread(_send_via_smtp, msg)
    logger.info("Password reset email sent to %s", to_email)


def _send_via_smtp(msg: EmailMessage) -> None:
    """Blocking SMTP conversation. Port 587 = plaintext connection upgraded
    to TLS via STARTTLS before any credentials are exchanged."""
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)


def _log_email(to_email: str, subject: str, body: str) -> None:
    logger.info(
        "\n────────── EMAIL (dev console fallback) ──────────\n"
        "To:      %s\n"
        "Subject: %s\n"
        "%s\n"
        "───────────────────────────────────────────────────",
        to_email, subject, body,
    )
