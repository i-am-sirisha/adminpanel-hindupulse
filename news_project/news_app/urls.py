from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('Staging_db', ApNewsViewSet,basename='Staging_db')
router.register('production_db', ProductionViewSet,basename='production_db')
router.register('staging_to_production', StagingToProductionViewSet,basename='staging_to_production')


urlpatterns = [
    path('', include(router.urls)),

]