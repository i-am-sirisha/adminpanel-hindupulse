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

 
    