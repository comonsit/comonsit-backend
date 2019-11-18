from rest_framework import serializers
from .models import Socios
from tsumbalil.serializers import ComunidadesSerializer
# from tsumbalil.models import Comunidades


class SociosSerializer(serializers.ModelSerializer):
    comunidad = ComunidadesSerializer()
    # comunidad = serializers.HyperlinkedRelatedField(queryset=Comunidades.objects.all(), view_name='comunidad-detail')
    cargo = serializers.SerializerMethodField()

    class Meta:
        model = Socios
        fields = ['clave_socio', 'nombres', 'apellidos', 'comunidad',
                  'curp', 'telefono', 'fecha_nacimiento', 'fecha_ingr_yomol_atel', 'fecha_ingr_programa',
                  'cargo', 'prod_trab', 'clave_anterior', 'estatus_cafe', 'estatus_miel',
                  'estatus_yip', 'estatus_gral']

    def get_cargo(self, socio):
        if socio.cargo:
            return '{0}'.format(socio.cargo.nombre_de_cargo)
        return ''
