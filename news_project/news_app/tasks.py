# your_app/tasks.py
from celery import shared_task
from .views import ApNewsViewSet
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_news_task():
    logger.info("Starting fetch_news_task")
    viewset = ApNewsViewSet()
    request = None  # Pass None as we are calling the method directly
    response = viewset.fetch_news(request)
    logger.info("Completed fetch_news_task")
    logger.info(f"Response data: {response.data}")
    return response.data  # or process the response as needed
