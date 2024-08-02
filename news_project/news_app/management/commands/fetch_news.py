# # news_app/management/commands/fetch_news.py
# from django.core.management.base import BaseCommand
# from news_app.views.apnews_views import ApNewsViewSet

# class Command(BaseCommand):
#     help = 'Fetches and stores news articles'

#     def handle(self, *args, **kwargs):
#         # Instantiate the viewset and call the fetch_news method
#         viewset = ApNewsViewSet()
#         viewset.fetch_news()
#         print("hhhhhhhhhhhhhhhhhhhhh")
#         self.stdout.write(self.style.SUCCESS('Successfully fetched and stored news articles'))
# news_app/management/commands/fetch_news.py

# import logging
# from django.core.management.base import BaseCommand
# from news_app.views.apnews_views import ApNewsViewSet

# # Set up logging
# logging.basicConfig(filename='fetch_news.log', level=logging.INFO)

# class Command(BaseCommand):
#     help = 'Fetches and stores news articles'

#     def handle(self, *args, **kwargs):
#         logging.info('Fetch news command started')
#         # Instantiate the viewset and call the core method directly
#         viewset = ApNewsViewSet()
#         viewset.process_news(None)  # No need to pass request here
#         logging.info('Successfully fetched and stored news articles')
