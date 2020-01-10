from rest_framework import serializers
from .models import Socio


class SocioSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField(read_only=True)
    nombre_comunidad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Socio
        fields = "__all__"

    def get_region(self, object):
        region = object.comunidad.region.id
        return region

    def get_nombre_comunidad(self, object):
        nombre_comunidad = object.comunidad.nombre_de_comunidad
        return nombre_comunidad
