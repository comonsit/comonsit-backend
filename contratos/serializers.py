from datetime import date
from rest_framework import serializers
from .models import ContratoCredito


class ContratoCreditoSerializer(serializers.ModelSerializer):
    promotor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     pass


class ContratoCreditoListSerializer(serializers.ModelSerializer):
    nombres = serializers.SerializerMethodField(read_only=True)
    tipo_credito = serializers.SerializerMethodField(read_only=True)
    estatus = serializers.SerializerMethodField(read_only=True)
    deuda_al_dia = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = ['folio', 'fecha_inicio', 'clave_socio', 'nombres',
                  'tipo_credito', 'monto', 'plazo', 'tasa', 'estatus',
                  'estatus_ejecucion', 'deuda_al_dia']

    def get_nombres(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellido_paterno \
                + ' ' + object.clave_socio.apellido_materno

    def get_tipo_credito(self, object):
        return object.solicitud.get_tipo_credito_display()

    def get_estatus(self, object):
        if object.estatus == ContratoCredito.DEUDA_PENDIENTE:
            if object.fecha_inicio:
                if object.fecha_inicio <= date.today():
                    return 'VI'  #VIGENTE
                return 'VE'  # VENCIDO
            return 'PF' #POR FIRMAR
        return object.estatus  # PAGADO

    def get_deuda_al_dia(self, object):
        # TODO: include moratorio, dynamic date and payments
        return object.monto + object.monto*(object.tasa/100)*object.plazo
