# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import StagingApNewsModel, ProductionApNewsModel
from ..serializers import StagingApNewsSerializer, ProductionApNewsSerializer








class ProductionViewSet(viewsets.ModelViewSet):
    queryset = StagingApNewsModel.objects.all()
    serializer_class = StagingApNewsSerializer

    @action(detail=False, methods=['post'])
    def transfer_to_production(self, request):
        _id = request.data.get('_id')
        print(f"Received ID: {_id}")  # Debugging line
        if not _id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            staging_record = StagingApNewsModel.objects.get(_id=_id)
        except StagingApNewsModel.DoesNotExist:
            return Response({"error": "Record not found in staging database"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the record already exists in production
        production_record, created = ProductionApNewsModel.objects.using('production_db').update_or_create(
            _id=staging_record._id,
            defaults={
                'headline': staging_record.headline,
                'summary': staging_record.summary,
                'link': staging_record.link,
                'image': staging_record.image,
                'url': staging_record.url,
            }
        )

        return Response({"message": "Data transferred to production successfully."}, status=status.HTTP_200_OK)
    



# class ProductionViewSet(viewsets.ModelViewSet):
#     queryset = StagingApNewsModel.objects.all()
#     serializer_class = StagingApNewsSerializer

#     @action(detail=False, methods=['post'])
#     def transfer_to_production(self, request):
#         staging_news = StagingApNewsModel.objects.all()
#         for news in staging_news:
#             production_news = ProductionApNewsModel(
#                 _id=news._id,
#                 headline=news.headline,
#                 summary=news.summary,
#                 link=news.link,
#                 image=news.image,
#                 url=news.url
#             )
#             production_news.save()
#         return Response({"message": "Data transferred to production successfully."}, status=status.HTTP_200_OK)






# class ProductionViewSet(viewsets.ModelViewSet):
#     queryset = StagingApNewsModel.objects.all()
#     serializer_class = StagingApNewsSerializer

#     @action(detail=False, methods=['post'])
#     def transfer_to_production(self, request):
#         _id = request.data.get('_id')
#         if not _id:
#             return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             staging_record = StagingApNewsModel.objects.get(_id=_id)
#         except StagingApNewsModel.DoesNotExist:
#             return Response({"error": "Record not found in staging database"}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the record already exists in production
#         production_record, created = ProductionApNewsModel.objects.update_or_create(
#             _id=staging_record._id,
#             defaults={
#                 'headline': staging_record.headline,
#                 'summary': staging_record.summary,
#                 'link': staging_record.link,
#                 'image': staging_record.image,
#                 'url': staging_record.url,
#             }
#         )

#         return Response({"message": "Data transferred to production successfully."}, status=status.HTTP_200_OK)
