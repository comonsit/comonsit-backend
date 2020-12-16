from rest_framework import serializers
from .models import InegiLocalidad, Zona


class InegiLocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InegiLocalidad
        fields = "__all__"


class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = "__all__"
