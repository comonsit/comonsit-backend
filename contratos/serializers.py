from datetime import date
from django.db.models import Sum
from rest_framework import serializers
from .models import ContratoCredito
from .utility import deuda_calculator
from pagos.models import Pago
from users.models import User


class ContratoCreditoSerializer(serializers.ModelSerializer):
    deuda_al_dia = serializers.SerializerMethodField(read_only=True)
    estatus_detail = serializers.SerializerMethodField(read_only=True)
    fecha_vencimiento = serializers.SerializerMethodField(read_only=True)
    nombres = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    comunidad = serializers.SerializerMethodField(read_only=True)
    proceso = serializers.SerializerMethodField(read_only=True)
    tipo_credito = serializers.SerializerMethodField(read_only=True)
    pagado = serializers.SerializerMethodField(read_only=True)
    plazo_disp = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = '__all__'
        extra_kwargs = {
            'estatus': {'read_only': True},
            'solicitud': {'read_only': True},
            'monto': {'read_only': True},
            'tasa': {'read_only': True},
            'tasa_moratoria': {'read_only': True},
            'fecha_final': {'read_only': True}
            }

    def get_deuda_al_dia(self, object):
        return deuda_calculator(object, date.today())

    def get_estatus_detail(self, object):
        return object.get_status()

    def get_fecha_vencimiento(self, object):
        return object.fecha_vencimiento()

    def get_nombres(self, object):
        return object.clave_socio.nombres_apellidos()

    def get_comunidad(self, object):
        return object.clave_socio.comunidad.nombre_de_comunidad

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id

    def get_proceso(self, object):
        return object.solicitud.get_proceso_display()

    def get_tipo_credito(self, object):
        return object.solicitud.get_tipo_credito_display()

    def get_pagado(self, object):
        return Pago.objects.filter(credito=object).aggregate(Sum('cantidad'))['cantidad__sum']

    def get_plazo_disp(self, object):
        prorroga = f'+{object.prorroga}' if object.prorroga > 0 else ''
        return str(object.plazo) + prorroga

    def update(self, instance, validated_data):
        current_user = self.context['request'].user
        # Signing Contract and starting Credit
        fecha_inicio = validated_data.get('fecha_inicio', None)
        tipo_tasa = validated_data.get('tipo_tasa', None)
        if fecha_inicio:
            if instance.fecha_inicio:
                raise serializers.ValidationError({"fecha_inicio": "Este cr??dito ya tiene fecha inicio"})
            else:
                instance.fecha_inicio = fecha_inicio
                instance.tipo_tasa = tipo_tasa

        # Updating Payment
        estatus_ejecucion = validated_data.get('estatus_ejecucion', None)
        referencia_banco = validated_data.get('referencia_banco', None)
        fecha_banco = validated_data.get('fecha_banco', None)
        if (estatus_ejecucion == ContratoCredito.POR_COBRAR and
                instance.estatus_ejecucion != ContratoCredito.POR_COBRAR):
            raise serializers.ValidationError({
                "estatus_ejecucion": "Un cr??dito no puede regresarse a estatus Por Cobrar"})
        # TODO: Check special cancellation case!
        elif (estatus_ejecucion == ContratoCredito.CANCELADO and
                current_user.role != User.ROL_GERENTE):
            raise serializers.ValidationError({"estatus_ejecucion": "S??lo un gerente puede CANCELAR"})
        instance.estatus_ejecucion = estatus_ejecucion
        instance.referencia_banco = referencia_banco
        instance.fecha_banco = fecha_banco

        instance.save()
        return instance


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
        fields = [
            'id', 'fecha_inicio', 'clave_socio', 'nombres',
            'monto', 'plazo_disp', 'tasa', 'estatus', 'estatus_ejecucion',
            'deuda_al_dia', 'region', 'fecha_vencimiento', 'pagado',
            'tasa_moratoria'
        ]

    def get_nombres(self, object):
        return object.clave_socio.nombres_apellidos()

    def get_estatus(self, object):
        return object.get_status()

    def get_deuda_al_dia(self, object):
        return deuda_calculator(object, date.today())

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
    pagado = serializers.SerializerMethodField(read_only=True)
    estatus_detail = serializers.SerializerMethodField(read_only=True)
    fecha_vencimiento = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = '__all__'

    # Method to calculate deuda once per object Serialization
    def to_representation(self, object):
        data = super().to_representation(object)
        deuda = deuda_calculator(object, date.today())
        deuda_keys = ['capital_por_pagar', 'interes_ordinario_deuda',
                      'interes_moratorio_deuda', 'total_deuda']
        for key in deuda_keys:
            if deuda:
                data[key] = deuda[key]
            else:
                data[key] = 0
        return data

    def get_nombres(self, object):
        return object.clave_socio.nombres_apellidos()

    def get_estatus_detail(self, object):
        return object.get_status()

    def get_fecha_vencimiento(self, object):
        return object.fecha_vencimiento().isoformat()

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


class ContratoUnLinkedSerializer(serializers.ModelSerializer):
    nombres = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    estatus = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = [
            'id', 'nombres', 'region', 'monto', 'fecha_inicio', 'fecha_banco',
            'referencia_banco', 'estatus', 'estatus_ejecucion'
        ]

    def get_nombres(self, object):
        return object.clave_socio.nombres_apellidos()

    def get_estatus(self, object):
        return object.get_status()

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id


class ContratoProrrogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoCredito
        fields = ['pk', 'prorroga', 'prorroga_justificacion']

    def validate_prorroga(self, prorroga):
        if not(1 <= prorroga <= 12):
            raise serializers.ValidationError("La pr??rroga debe ser entre 1 y 12 meses m??ximo")
        if self.instance.prorroga:
            raise serializers.ValidationError("El cr??dito ya tiene una pr??rroga y no se puede otorgar otra.")
        return prorroga

    def update(self, instance, validated_data):
        prorroga = validated_data.pop('prorroga')
        prorroga_justificacion = validated_data.pop('prorroga_justificacion')
        if instance.estatus != ContratoCredito.DEUDA_PENDIENTE:
            raise serializers.ValidationError("El Cr??dito no est?? corriendo y no se puede otorgar una pr??rroga")
        if instance.estatus_ejecucion != ContratoCredito.COBRADO:
            raise serializers.ValidationError("El Cr??dito no ha sido cobrado y no se puede otorgar una pr??rroga")
        else:
            instance.prorroga = prorroga
            instance.prorroga_justificacion = prorroga_justificacion
        instance.save()
        return instance
