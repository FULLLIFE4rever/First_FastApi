from celery import Celery
from celery.schedules import crontab

from config import settings

celery_worker = Celery(
    "tasks",
    broker=settings.redis_url,
    include=["tasks.tasks", "tasks.scheduled"],
)

celery_worker.conf.beat_schedule = {
    "before_3_days": {
        "task": "periodic_task",
        "schedule": crontab(hour='15', minute='00', day_of_month='*/1'),
        "args": (3,)
    },
    "before_1_days": {
        "task": "periodic_task",
        "schedule": crontab(hour='9', minute='30', day_of_month='*/1'),
        "args": (1,)
    }
}
