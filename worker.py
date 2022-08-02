from typing import Optional

from celery import Celery

import config
from src.base.entrypoints.schemas import File
from src.base.send_email import Email

celery_config = config.get_celery_settings()
celery = Celery(__name__, broker=celery_config.broker, backend=celery_config.result)


@celery.task(name='send_email', autoretry_for=(Exception,), max_retries=5, retry_kwargs={'countdown': 5})
def send_email_task(
    *,
    subject: str,
    recipient: str,
    text: str,
    html: Optional[str] = None,
    files: Optional[list[File]] = None,
) -> None:
    Email.send(subject=subject, recipient=recipient, text=text, html=html, files=files)
