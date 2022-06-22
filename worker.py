from celery import Celery

import config

celery_config = config.get_celery_settings()
celery = Celery(__name__, broker=celery_config.broker, backend=celery_config.result)
