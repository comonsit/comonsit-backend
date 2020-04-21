from django.db.models import Sum
from rest_framework import serializers
from .models import ContratoCredito
from .utility import deuda_calculator
from pagos.models import Pago


class ContratoCreditoSerializer(serializers.ModelSerializer):
    deuda_al_dia = serializers.SerializerMethodField(read_only=True)
    estatus_detail = serializers.SerializerMethodField(read_only=True)
    fecha_vencimiento = serializers.SerializerMethodField(read_only=True)
    nombres = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    comunidad = serializers.SerializerMethodField(read_only=True)
    proceso = serializers.SerializerMethodField(read_only=True)
    tipo_credito = serializers.SerializerMethodField(read_only=True)
    intereses = serializers.SerializerMethodField(read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    pagado = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = '__all__'

    def get_deuda_al_dia(self, object):
        return deuda_calculator(object)

    def get_estatus_detail(self, object):
        return object.get_validity()

    def get_fecha_vencimiento(self, object):
        return object.fecha_vencimiento()

    def get_nombres(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellido_paterno \
                + ' ' + object.clave_socio.apellido_materno

    def get_comunidad(self, object):
        return object.clave_socio.comunidad.nombre_de_comunidad

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id

    def get_proceso(self, object):
        return object.solicitud.get_proceso_display()

    def get_tipo_credito(self, object):
        return object.solicitud.get_tipo_credito_display()

    # TODO: Check if should use deuda_calculator instead!!
    # with the next two
    def get_intereses(self, object):
        return object.monto*(object.tasa/100)*object.plazo

    def get_total(self, object):
        return object.monto + object.monto*(object.tasa/100)*object.plazo

    def get_pagado(self, object):
        return Pago.objects.filter(credito=object).aggregate(Sum('cantidad'))['cantidad__sum']

    # def update(self, instance, validated_data):
    #     pass


class ContratoCreditoListSerializer(serializers.ModelSerializer):
    nombres = serializers.SerializerMethodField(read_only=True)
    estatus = serializers.SerializerMethodField(read_only=True)
    deuda_al_dia = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    fecha_vencimiento = serializers.SerializerMethodField(read_only=True)
    plazo_disp = serializers.SerializerMethodField(read_only=True)
    pagado = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = ['folio', 'fecha_inicio', 'clave_socio', 'nombres',
                  'monto', 'plazo_disp', 'tasa', 'estatus', 'estatus_ejecucion',
                  'deuda_al_dia', 'region', 'fecha_vencimiento', 'pagado',
                  'tasa_moratoria']

    def get_nombres(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellido_paterno \
                + ' ' + object.clave_socio.apellido_materno

    def get_estatus(self, object):
        return object.get_validity()

    def get_deuda_al_dia(self, object):
        return deuda_calculator(object)

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id

    def get_plazo_disp(self, object):
        prorroga = f'+{object.prorroga}' if object.prorroga > 0 else ''
        return str(object.plazo) + prorroga

    def get_fecha_vencimiento(self, object):
        return object.fecha_vencimiento()

    def get_pagado(self, object):
        return Pago.objects.filter(credito=object).aggregate(Sum('cantidad'))['cantidad__sum']


class ContratoXLSXSerializer(serializers.ModelSerializer):
    nombres = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    comunidad = serializers.SerializerMethodField(read_only=True)
    amortizado = serializers.SerializerMethodField(read_only=True)
    tipo_credito = serializers.SerializerMethodField(read_only=True)
    deuda_al_dia = serializers.SerializerMethodField(read_only=True)
    estatus_detail = serializers.SerializerMethodField(read_only=True)
    fecha_vencimiento = serializers.SerializerMethodField(read_only=True)
    pagado = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = '__all__'

    def get_nombres(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellido_paterno \
                + ' ' + object.clave_socio.apellido_materno

    def get_deuda_al_dia(self, object):
        deuda = deuda_calculator(object)
        if deuda:
            return deuda['total']
        return 0

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

    def get_pagado(self, object):
        return Pago.objects.filter(credito=object).aggregate(Sum('cantidad'))['cantidad__sum']
