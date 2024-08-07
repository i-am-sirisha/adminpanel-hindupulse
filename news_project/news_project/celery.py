# # your_project/celery.py
# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')

# app = Celery('news_project')

# # Using a string here means the worker doesn’t have to serialize
# # the configuration object to child processes.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()

from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings') # project name.settings

app = Celery('news_project') # provide your project name
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

app.conf.beat_schedule = {
# create an object for your scheduling your task
    'fetch-and-store-temp-data-contrab': {
        'task': 'news_app.tasks.fetch_news_task', #app_name.tasks.function_name
        'schedule': crontab(minute='*/5'), #crontab() means run every minute
        # 'args' : (..., ...) In case function takes parameters, add them here
    }
}