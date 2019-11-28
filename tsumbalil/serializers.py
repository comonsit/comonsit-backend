from rest_framework import serializers
from .models import Cargo, Region, Comunidad


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['nombre_de_cargo']
        read_only_fields = ['nombre_de_cargo']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['nombre_de_region']
        read_only_fields = ['nombre_de_region']


class ComunidadSerializer(serializers.ModelSerializer):
    nombre_region = serializers.CharField(source='region.nombre_de_region', read_only=True)

    class Meta:
        model = Comunidad
        fields = "__all__"
