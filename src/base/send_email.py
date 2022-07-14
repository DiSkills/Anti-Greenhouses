import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Union

import config
from src.base.schemas import File

email_config = config.get_email_settings()


class Email:

    @staticmethod
    def _send(*, message: MIMEMultipart) -> None:
        server = smtplib.SMTP(email_config.host, email_config.port)
        server.starttls()

        try:
            server.login(email_config.sender_email, email_config.sender_password)
            server.sendmail(message['From'], message['To'], message.as_string())
        finally:
            server.quit()

    @staticmethod
    def _create_message(*, subject: str, recipient: str) -> MIMEMultipart:
        message = MIMEMultipart()

        message['Subject'] = subject
        message['From'] = email_config.sender_email
        message['To'] = recipient

        return message

    @staticmethod
    def _add_payload(*, message: MIMEMultipart, text: str, files: list[File], html: Optional[str] = None) -> None:
        attachments: list[Union[MIMEText, MIMEBase]] = []

        if html is not None:
            attachments.append(MIMEText(html, 'html'))
        else:
            attachments.append(MIMEText(text, 'plain'))

        for file in files:
            _attachment = MIMEBase(file.type, file.subtype)
            _attachment.set_payload(file.content)
            encoders.encode_base64(_attachment)

            _attachment.add_header('content-disposition', 'attachment', filename=file.filename)

            attachments.append(_attachment)

        for attachment in attachments:
            message.attach(attachment)

    @classmethod
    def send(
        cls,
        *,
        subject: str,
        recipient: str,
        text: str,
        html: Optional[str] = None,
        files: Optional[list[File]] = None,
    ) -> None:
        message = cls._create_message(subject=subject, recipient=recipient)

        if files is None:
            files = []

        cls._add_payload(message=message, text=text, html=html, files=files)

        cls._send(message=message)


def send_email(
    *,
    subject: str,
    recipient: str,
    text: str,
    html: Optional[str] = None,
    files: Optional[list[File]] = None,
) -> None:
    from worker import send_email_task
    send_email_task.delay(subject=subject, recipient=recipient, text=text, html=html, files=files)
