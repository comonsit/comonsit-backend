from rest_framework import serializers
from .models import Acopio


class AcopioSerializer(serializers.ModelSerializer):
    nombre_socio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Acopio
        fields = "__all__"

    def get_nombre_socio(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellidos
