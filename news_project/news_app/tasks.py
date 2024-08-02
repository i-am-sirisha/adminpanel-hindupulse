from celery import shared_task
from news_app.views.apnews_views import ApNewsViewSet

@shared_task
def fetch_and_store_news():
    viewset = ApNewsViewSet()
    print("@@@@@@@@@@@@@",viewset)
    viewset.process_news(None)  # Adjust according to your method
