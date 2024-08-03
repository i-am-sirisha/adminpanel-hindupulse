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
# celery.py or tasks.py
# from celery import Celery
# from celery.schedules import crontab

# app = Celery('news_project')

# app.conf.beat_schedule = {
#     'fetch-news-every-10-minutes': {
#         'task': 'news_app.tasks.fetch_and_store_news',
#         'schedule': crontab(minute='*/10'),
#     },
# }



from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')

app = Celery('news_project')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-news-every-10-minutes': {
        'task': 'news_app.tasks.fetch_and_store_news',
        'schedule': crontab(minute='*/10'),
    },
}