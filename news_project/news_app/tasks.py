# from celery import shared_task
# from news_app.views.apnews_views import ApNewsViewSet

# @shared_task
# def fetch_and_store_news():
#     viewset = ApNewsViewSet()
#     print("@@@@@@@@@@@@@",viewset)
#     viewset.process_news(None)  # Adjust according to your method

from celery import shared_task
from news_app.views.apnews_views import ApNewsViewSet

@shared_task
def fetch_and_store_news():
    viewset = ApNewsViewSet()
    try:
        response = viewset.process_news()
        print("News data successfully processed and saved.")
    except Exception as e:
        print(f"Failed to process and save news data: {e}")