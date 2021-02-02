from rest_framework import serializers
from .models import InegiLocalidad, Zona, Ermita


class InegiLocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InegiLocalidad
        fields = "__all__"


class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = "__all__"


class ErmitaListSerializer(serializers.ModelSerializer):
    zona = serializers.SerializerMethodField(read_only=True)
    interzona = serializers.SerializerMethodField(read_only=True)
    municipio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ermita
        fields = ["ermita_id", "zona", "interzona",
                  "municipio", "nombre", "localidad"]

    def get_zona(self, object):
        if object.zona:
            return object.zona.nombre
        return None

    def get_interzona(self, object):
        if object.zona:
            return object.zona.interzona.nombre
        return None

    def get_municipio(self, object):
        if object.municipio:
            return object.municipio.nombre
        return None


class ErmitaSerializer(ErmitaListSerializer):
    ubicacion = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ermita
        fields = "__all__"

    def get_ubicacion(self, object):
        if object.localidad:
            return [object.localidad.ubicacion.y, object.localidad.ubicacion.x]
        return None
