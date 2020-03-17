from rest_framework import serializers
from .models import Cargo, CargoCoop, Region, Comunidad, Empresa, Puesto_Trabajo, Fuente


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__"


class CargoCoopSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoCoop
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class ComunidadSerializer(serializers.ModelSerializer):
    nombre_region = serializers.CharField(source='region.nombre_de_region', read_only=True)

    class Meta:
        model = Comunidad
        fields = "__all__"


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = "__all__"


class PuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puesto_Trabajo
        fields = "__all__"


class FuenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuente
        fields = "__all__"
