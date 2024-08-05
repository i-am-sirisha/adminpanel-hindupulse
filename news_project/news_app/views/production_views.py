# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import StagingApNewsModel, ProductionApNewsModel
from ..serializers import StagingApNewsSerializer, ProductionApNewsSerializer
from django.shortcuts import get_object_or_404




class StagingToProductionViewSet(viewsets.ModelViewSet):
    queryset = StagingApNewsModel.objects.all()
    serializer_class = StagingApNewsSerializer

    @action(detail=False, methods=['post'], url_path='transfer_to_production/(?P<_id>[^/.]+)')
    def transfer_to_production(self, request, _id=None):
        if not _id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            staging_record = get_object_or_404(StagingApNewsModel, _id=_id)
        except StagingApNewsModel.DoesNotExist:
            return Response({"error": "Record not found in staging database"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Check if the record already exists in production
            production_record, created = ProductionApNewsModel.objects.using('production_db').update_or_create(
                _id=staging_record._id,
                defaults={
                    'headline': staging_record.headline,
                    'summary': staging_record.summary,
                    'link': staging_record.link,
                    'image': staging_record.image,
                    'url': staging_record.url,
                    'category_id': staging_record.category,
                    'news_sub_category_id': staging_record.subcategory,
                }
            )
            message = "Data transferred to production successfully." if created else "Data updated in production successfully."
            return Response({"message": message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductionViewSet(viewsets.ModelViewSet):
    queryset = ProductionApNewsModel.objects.all()
    serializer_class = ProductionApNewsSerializer