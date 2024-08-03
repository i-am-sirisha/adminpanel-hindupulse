# from celery import shared_task
# from news_app.views.apnews_views import ApNewsViewSet

# @shared_task
# def fetch_and_store_news():
#     viewset = ApNewsViewSet()
#     print("@@@@@@@@@@@@@",viewset)
#     viewset.process_news(None)  # Adjust according to your method

# from celery import shared_task
# from news_app.views.apnews_views import ApNewsViewSet

# @shared_task
# def fetch_and_store_news():
#     viewset = ApNewsViewSet()
#     try:
#         response = viewset.process_news()
#         print("News data successfully processed and saved.")
#     except Exception as e:
#         print(f"Failed to process and save news data: {e}")

# tasks.py
# tasks.py
# news_app/tasks.py

from celery import shared_task
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_and_store_news():
    logger.info('Starting fetch_and_store_news task')
    try:
        result = subprocess.run(['python', 'manage.py', 'fetch_news'], capture_output=True, text=True)
        logger.info('fetch_and_store_news task completed with output: %s', result.stdout)
        if result.stderr:
            logger.error('fetch_and_store_news task encountered errors: %s', result.stderr)
    except Exception as e:
        logger.error('Error running fetch_and_store_news task: %s', e)
