from celery.schedules import crontab
from celery import shared_task
from celery.utils.log import get_task_logger

from sheets import statistics


@shared_task(
	run_every=(crontab(minute="*/15")),
	name="save_stats_task",
	ignore_result=True
	)
def save_stats_task():
	statistics()



