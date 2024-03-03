from celery import Celery
from celery.schedules import crontab

from config import settings

celery_worker = Celery(
    "tasks",
    broker=settings.redis_url,
    include=["tasks.tasks", "tasks.scheduled"],
)

celery_worker.conf.beat_schedule = {
    "name": {
        "task": "periodic_task",
        "schedule": crontab(),
    }
}
