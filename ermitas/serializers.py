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


class ErmitaSerializer(serializers.ModelSerializer):
    zona = serializers.SerializerMethodField(read_only=True)
    interzona = serializers.SerializerMethodField(read_only=True)
    municipio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ermita
        fields = "__all__"

    def get_zona(self, object):
        if object.zona:
            return str(object.zona)
        return None

    def get_interzona(self, object):
        if object.zona:
            return str(object.zona.interzona)
        return None

    def get_municipio(self, object):
        if object.municipio:
            return str(object.municipio)
        return None
