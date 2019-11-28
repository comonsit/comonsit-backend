from rest_framework import serializers
from .models import Socio


class SocioSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Socio
        fields = "__all__"

    def get_region(self, object):
        region = object.comunidad.region.nombre_de_region
        return region
