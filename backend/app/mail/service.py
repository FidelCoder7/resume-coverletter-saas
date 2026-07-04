import smtplib
from email.message import EmailMessage

from app.core.config import settings


class MailService:
    """
    SMTP mail service.

    Uses Mailtrap during development and can later
    be pointed to any SMTP provider.
    """

    def send(
        self,
        *,
        recipient: str,
        subject: str,
        body: str,
        html: str | None = None,
    ) -> None:
        message = EmailMessage()

        message["Subject"] = subject
        message["From"] = settings.MAIL_FROM
        message["To"] = recipient

        message.set_content(body)

        if html:
            message.add_alternative(
                html,
                subtype="html",
            )

        with smtplib.SMTP(
            settings.MAIL_HOST,
            settings.MAIL_PORT,
        ) as smtp:
            smtp.starttls()

            smtp.login(
                settings.MAIL_USERNAME,
                settings.MAIL_PASSWORD,
            )

            smtp.send_message(message)
