import os
from celery import Celery
from sheets.check_links import LinkChecker
import datetime

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edu_test.settings')

app = Celery('edu_test')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
#app.autodiscover_tasks()


"""@app.task(bind=True)
def debug_task(self):
	print(f'Request: {self.request!r}')"""

@app.task(bind=True)
def write_sheet(self):
	a = LinkChecker()
	a.check()

@app.task()
def write_text(self):
	self.s = 'Пишем ерунду в файл'
	with open('text.txt', 'a') as f:
		f.write(self.s, datetime.datetime)