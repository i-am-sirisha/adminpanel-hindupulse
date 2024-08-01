
from rest_framework import serializers
from ..models import ProductionApNewsModel

class ProductionApNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionApNewsModel
        fields = "__all__"