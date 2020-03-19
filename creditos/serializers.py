from rest_framework import serializers
from .models import SolicitudCredito
from socios.serializers import SocioSerializer
from users.models import User


class SolicitudCreditoSerializer(serializers.ModelSerializer):
    promotor = serializers.StringRelatedField(read_only=True)
    nombre_productor = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    comunidad = serializers.SerializerMethodField(read_only=True)
    # area = serializers.SerializerMethodField(read_only=True)
    aval_nombre = serializers.SerializerMethodField(read_only=True)
    cargo = serializers.SerializerMethodField(read_only=True)
    cargo_coop = serializers.SerializerMethodField(read_only=True)
    # cargo_mision = serializers.SerializerMethodField(read_only=True)
    fecha_ingr_yomol_atel = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SolicitudCredito
        fields = '__all__'

    def get_nombre_productor(self, object):
        return object.clave_socio.nombres + ' ' + object.aval.apellido_paterno +' ' + object.aval.apellido_materno

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id

    def get_comunidad(self, object):
        return object.clave_socio.comunidad.nombre_de_comunidad

    def get_aval_nombre(self, object):
        return object.aval.nombres + ' ' + object.aval.apellido_paterno + ' ' + object.aval.apellido_materno

    def get_cargo(self, object):
        return object.clave_socio.cargo.nombre_de_cargo

    def get_cargo_coop(self, object):
        return ', '.join([c.nombre_cargo_coop for c in object.clave_socio.cargo_coop.all()])

    def get_fecha_ingr_yomol_atel(self, object):
        return object.clave_socio.fecha_ingr_yomol_atel

    def validate(self, data):
        """
        Check that requestor and authorizor are not the same
        """
        if data['clave_socio'] == data['aval']:
            raise serializers.ValidationError("Aval y Solicitante deben ser diferentes")
        """
        Check for recent duplicates
        """
        if SolicitudCredito.objects.filter(
           clave_socio=data['clave_socio']).filter(
           fecha_solicitud=data['fecha_solicitud']).filter(
           monto_solicitado=data['monto_solicitado']):
            raise serializers.ValidationError("Ya existe un crédito con esa fecha y monto")

        return data


class SolicitudListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudCredito
        fields = ['folio_solicitud', 'fecha_solicitud', 'clave_socio', 'tipo_credito',
                  'plazo_de_pago_solicitado', 'estatus_solicitud', 'estatus_ej_credito']


class SolicitudPartialUpdateSerializer(serializers.ModelSerializer):
    promotor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SolicitudCredito
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        print('EL ROL ES:')
        print(user.role)
        return data
