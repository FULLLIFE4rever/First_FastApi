from tasks.celery_conf import celery_worker


@celery_worker.task(name="periodic_task")
def pereodic_task():
    print(12345)
