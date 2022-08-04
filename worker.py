from typing import Optional

from celery import Celery

import config
from src.base.entrypoints.schemas import File
from src.base.send_email import Email
from src.base.uow import UnitOfWork

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


@celery.task(name='remove_bad_login', autoretry_for=(Exception,), max_retries=5, retry_kwargs={'countdown': 5})
def remove_bad_login_task(*, uuid: str) -> None:
    with UnitOfWork() as uow:
        uow.bad_logins.remove(uuid=uuid)


def remove_bad_login(*, uuid: str) -> None:
    remove_bad_login_task.apply_async(kwargs={'uuid': uuid}, countdown=celery_config.bad_login_countdown)
