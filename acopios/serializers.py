from rest_framework import serializers
from .models import Acopios


class AcopiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acopios
        fields = ['id', 'fecha', 'ingreso', 'kilosDeProducto', 'tipoDeProducto']
