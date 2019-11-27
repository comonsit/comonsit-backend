from rest_framework import serializers
from .models import Acopio


class AcopioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acopio
        fields = ['id', 'fecha', 'ingreso', 'kilos_de_producto', 'tipo_de_producto']
