from rest_framework import serializers
from .models import Acopio


class AcopioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acopio
        fields = "__all__"
