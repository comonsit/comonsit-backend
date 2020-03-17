from rest_framework import serializers
from .models import Socio


class SocioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Socio
        fields = "__all__"



class SocioListSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField(read_only=True)
    nombre_comunidad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Socio
        fields = [
            "clave_socio", "nombres", "apellido_paterno", "apellido_materno",
            "region", "nombre_comunidad", "clave_anterior", "estatus_cafe",
            "estatus_miel", "estatus_yip", "estatus_trabajador", "estatus_gral",
            "created", "updated"
        ]

    def get_region(self, object):
        region = object.comunidad.region.id
        return region

    def get_nombre_comunidad(self, object):
        nombre_comunidad = object.comunidad.nombre_de_comunidad
        return nombre_comunidad
