from rest_framework import serializers
from .models import ContratoCredito
from .utility import deuda_calculator


class ContratoCreditoSerializer(serializers.ModelSerializer):
    deuda_al_dia = serializers.SerializerMethodField(read_only=True)
    estatus_detail = serializers.SerializerMethodField(read_only=True)
    fecha_vencimiento = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = '__all__'

    def get_deuda_al_dia(self, object):
        return deuda_calculator(object)

    def get_estatus_detail(self, object):
        return object.get_validity()

    def get_fecha_vencimiento(self, object):
        return object.fecha_vencimiento()

    # def update(self, instance, validated_data):
    #     pass


class ContratoCreditoListSerializer(serializers.ModelSerializer):
    nombres = serializers.SerializerMethodField(read_only=True)
    tipo_credito = serializers.SerializerMethodField(read_only=True)
    estatus = serializers.SerializerMethodField(read_only=True)
    deuda_al_dia = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = ['folio', 'fecha_inicio', 'clave_socio', 'nombres',
                  'tipo_credito', 'monto', 'plazo', 'tasa', 'estatus',
                  'estatus_ejecucion', 'deuda_al_dia', 'region']

    def get_nombres(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellido_paterno \
                + ' ' + object.clave_socio.apellido_materno

    def get_tipo_credito(self, object):
        return object.solicitud.get_tipo_credito_display()

    def get_estatus(self, object):
        return object.get_validity()

    def get_deuda_al_dia(self, object):
        return deuda_calculator(object)

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id


class ContratoXLSXSerializer(serializers.ModelSerializer):
    nombres = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    comunidad = serializers.SerializerMethodField(read_only=True)
    amortizado = serializers.SerializerMethodField(read_only=True)
    tipo_credito = serializers.SerializerMethodField(read_only=True)
    deuda_al_dia = serializers.SerializerMethodField(read_only=True)
    estatus_detail = serializers.SerializerMethodField(read_only=True)
    fecha_vencimiento = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = '__all__'

    def get_nombres(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellido_paterno \
                + ' ' + object.clave_socio.apellido_materno

    def get_deuda_al_dia(self, object):
        return deuda_calculator(object)

    def get_estatus_detail(self, object):
        return object.get_validity()

    def get_fecha_vencimiento(self, object):
        return object.fecha_vencimiento()

    def get_comunidad(self, object):
        return object.clave_socio.comunidad.nombre_de_comunidad

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id

    def get_amortizado(self, object):
        return 'PENDIENTE'

    def get_tipo_credito(self, object):
        return object.solicitud.get_tipo_credito_display()
