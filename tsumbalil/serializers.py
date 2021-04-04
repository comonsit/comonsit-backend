from rest_framework import serializers
from .models import Cargo, CargoCoop, Region, Comunidad, Empresa, \
                    Puesto_Trabajo, Fuente


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__"


class CargoCoopSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoCoop
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class ComunidadSerializer(serializers.ModelSerializer):
    nombre_region = serializers.CharField(source='region.nombre_de_region', read_only=True)
    ubicacion = serializers.SerializerMethodField(read_only=True)
    ermita_name = serializers.SerializerMethodField(read_only=True)
    inegiLocalidad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comunidad
        fields = "__all__"

    def get_ubicacion(self, object):
        if object.ermita and object.ermita.localidad:
            # return f'lat: {object.ermita.localidad.ubicacion.x} lon: {object.ermita.localidad.ubicacion.y}'
            return [object.ermita.localidad.ubicacion.y, object.ermita.localidad.ubicacion.x]
        elif object.inegi_extra:
            return [object.inegi_extra.ubicacion.y, object.inegi_extra.ubicacion.x]
        return None

    def get_ermita_name(self, object):
        if object.ermita:
            return str(object.ermita.ermita_id) + ': ' + object.ermita.nombre
        return None

    def get_inegiLocalidad(self, object):
        if object.ermita and object.ermita.localidad:
            return object.ermita.localidad.localidad_id


class ComunidadSociosSerializer(serializers.ModelSerializer):
    num_socios_cf = serializers.IntegerField()
    num_socios_mi = serializers.IntegerField()
    num_socios_ja = serializers.IntegerField()
    num_socios_sl = serializers.IntegerField()
    ubicacion = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comunidad
        fields = ['id', 'nombre_de_comunidad', 'num_socios_cf',
                  'num_socios_mi', 'num_socios_ja', 'num_socios_sl', 'ubicacion']

    def get_ubicacion(self, object):
        if object.ermita and object.ermita.localidad:
            return [object.ermita.localidad.ubicacion.y, object.ermita.localidad.ubicacion.x]
        elif object.inegi_extra:
            return [object.inegi_extra.ubicacion.y, object.inegi_extra.ubicacion.x]
        return None


class ComunidadSerializerXLSX(ComunidadSerializer):
    ubicacion = None
    latitud = serializers.SerializerMethodField(read_only=True)
    longitud = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comunidad
        fields = "__all__"

    def get_latitud(self, object):
        if object.ermita and object.ermita.localidad:
            return object.ermita.localidad.ubicacion.y
        elif object.inegi_extra:
            return object.inegi_extra.ubicacion.y
        return None

    def get_longitud(self, object):
        if object.ermita and object.ermita.localidad:
            return object.ermita.localidad.ubicacion.x
        elif object.inegi_extra:
            return object.inegi_extra.ubicacion.x
        return None


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = "__all__"


class PuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puesto_Trabajo
        fields = "__all__"


class FuenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuente
        fields = "__all__"
