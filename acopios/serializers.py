from rest_framework import serializers
from .models import Acopio


class AcopioSerializer(serializers.ModelSerializer):
    nombre_socio = serializers.SerializerMethodField(read_only=True)
    comunidad = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Acopio
        fields = "__all__"

    def get_nombre_socio(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellidos

    def get_comunidad(self, object):
        return object.clave_socio.comunidad.nombre_de_comunidad

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id


class AcopioTotalsSerializer(serializers.ModelSerializer):
    fecha__year = serializers.IntegerField()
    year_sum = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Acopio
        fields = ['fecha__year', 'year_sum']
