from rest_framework import serializers
from core.models import Enginetempstorage

class EngineTempStorageAgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enginetempstorage
        fields = ["Image"]
    
    