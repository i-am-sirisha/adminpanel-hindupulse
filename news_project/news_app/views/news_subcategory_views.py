from rest_framework import viewsets
from ..models import NewsSubCategory
from ..serializers import NewsSubCategorySerializer
# from ..pagination import CustomPagination 
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.views import APIView
from rest_framework import status





class NewsSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = NewsSubCategory.objects.all().order_by("name")
    serializer_class = NewsSubCategorySerializer
    # pagination_class = CustomPagination

class GetSubCategoryById_InputView(APIView):
    def get(self, request, _id):
        try:
            # Fetch the queryset without pagination
            filter_kwargs = {"other_category": _id}
            queryset = NewsSubCategory.objects.filter(**filter_kwargs)

            # Serialize the data
            serialized_data = NewsSubCategorySerializer(queryset, many=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)

        except NewsSubCategory.DoesNotExist:
            return Response({
                'message': 'Object not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

 
    