from rest_framework import serializers
from ..models import *

class ApNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApNewsModel
        fields = "__all__"