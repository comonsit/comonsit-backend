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
            "estatus_miel", "estatus_yip", "estatus_trabajador", "estatus_comonSit",
            "created", "updated"
        ]

    def get_region(self, object):
        region = object.comunidad.region.id
        return region

    def get_nombre_comunidad(self, object):
        nombre_comunidad = object.comunidad.nombre_de_comunidad
        return nombre_comunidad


class SocioSerializerXLS(serializers.ModelSerializer):
    cargo_coop = serializers.SerializerMethodField(read_only=True)
    empresa = serializers.StringRelatedField()
    cargo = serializers.StringRelatedField()
    puesto = serializers.StringRelatedField()
    comunidad = serializers.StringRelatedField()

    class Meta:
        model = Socio
        fields = [
            "clave_socio", "nombres", "apellido_paterno", "apellido_materno",
            "comunidad", "curp", "genero", "telefono", "clave_anterior", "fecha_nacimiento",
            "fecha_ingr_yomol_atel", "fecha_ingr_programa", "cargo", "cargo_coop",
            "empresa", "puesto", "fuente", "estatus_cafe", "estatus_miel", "estatus_yip",
            "estatus_trabajador", "estatus_comonSit", "doc_curp", "doc_act_nac", "doc_ine",
            "doc_domicilio", "created", "updated"
        ]

    def get_cargo_coop(self, object):
        return ', '.join([c.nombre_cargo_coop for c in object.cargo_coop.all()])
