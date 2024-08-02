from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('Staging_db', ApNewsViewSet,basename='Staging_db')
router.register('production_db', ProductionViewSet,basename='production_db')
# production_transfer = ProductionViewSet.as_view({'post': 'transfer_to_production'})

urlpatterns = [
    path('', include(router.urls)),
    # path('staging_to_production_db/<uuid:_id>/', production_transfer, name='staging_to_production_db'),
]
# router.register('production_db', ProductionViewSet,basename='production_db')

# urlpatterns = [
#     path('', include(router.urls)),
# ]