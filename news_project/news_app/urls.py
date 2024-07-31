from django.urls import path
from .views import FetchNewsView

urlpatterns = [
    
    path('fetch_news/', FetchNewsView.as_view(), name='fetch_news'),
]
