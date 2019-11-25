from rest_framework import serializers
from .models import Socios
from tsumbalil.serializers import ComunidadesSerializer
# from tsumbalil.models import Comunidades


class SociosSerializer(serializers.ModelSerializer):
    comunidad_id = ComunidadesSerializer(source='comunidad', read_only=True)
    cargo_id = serializers.SerializerMethodField(source='cargo', read_only=True)

    class Meta:
        model = Socios
        fields = ['clave_socio', 'nombres', 'apellidos', 'comunidad_id',
                  'curp', 'telefono', 'fecha_nacimiento', 'fecha_ingr_yomol_atel', 'fecha_ingr_programa',
                  'cargo_id', 'prod_trab', 'clave_anterior', 'estatus_cafe', 'estatus_miel',
                  'estatus_yip', 'estatus_gral']

    def get_cargo_id(self, socio):
        if socio.cargo:
            return '{0}'.format(socio.cargo.nombre_de_cargo)
        return ''
