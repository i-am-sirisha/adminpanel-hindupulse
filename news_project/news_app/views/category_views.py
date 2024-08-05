from rest_framework import viewsets
from ..models import *
from ..serializers import *
from rest_framework.views import *


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('priority_order')
    serializer_class = CategorySerializer
