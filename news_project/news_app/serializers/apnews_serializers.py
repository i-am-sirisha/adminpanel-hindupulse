from rest_framework import serializers
from ..models import *

class StagingApNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StagingApNewsModel
        fields = "__all__"