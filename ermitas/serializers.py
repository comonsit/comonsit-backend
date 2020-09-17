from rest_framework import serializers
from .models import InegiLocalidad


class InegiLocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InegiLocalidad
        fields = "__all__"
