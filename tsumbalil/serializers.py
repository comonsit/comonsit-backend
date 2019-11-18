from rest_framework import serializers
from .models import Cargos, Regiones, Comunidades


class CargosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargos
        fields = ['nombre_de_cargo']


class RegionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regiones
        fields = ['nombre_de_region']


class ComunidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunidades
        fields = ['nombre_de_comunidad', 'region']
