from rest_framework import serializers
from .models import Socio
from tsumbalil.serializers import ComunidadSerializer
# from tsumbalil.models import Comunidad


class SocioSerializer(serializers.ModelSerializer):
    comunidad_id = ComunidadSerializer(source='comunidad', read_only=True)
    # cargo = serializers.StringRelatedField()

    class Meta:
        model = Socio
        fields = ['clave_socio', 'nombres', 'apellidos', 'comunidad_id',
                  'curp', 'telefono', 'fecha_nacimiento', 'fecha_ingr_yomol_atel', 'fecha_ingr_programa',
                  'cargo', 'prod_trab', 'clave_anterior', 'estatus_cafe', 'estatus_miel',
                  'estatus_yip', 'estatus_gral']
