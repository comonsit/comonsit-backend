from datetime import date
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from .models import Movimiento
from comonSitDjango.constants import PROCESOS_FIELDS, ACTIVO


class MovimientoSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Movimiento
        fields = "__all__"

    def validate(self, data):
        """
        Check that user is active in requested process
        """
        socio = data.get('clave_socio')
        process_status = getattr(socio, PROCESOS_FIELDS[data['proceso']])
        if process_status != ACTIVO:
            raise serializers.ValidationError("El Socio no está activo en este proceso")

        aportacion = data.get('aportacion')
        monto = data.get('monto')
        current_user = self.context['request'].user
        # Validation for RETIROS
        if not aportacion:
            # only Gerencia can save RETIROS
            if not current_user.is_gerencia():
                raise serializers.ValidationError("Solo gerencia puede registrar Retiros")

            # RETIRO Cannot by greater than available balance
            q = Movimiento.objects.filter(clave_socio=socio)
            aports = q.filter(aportacion=True).aggregate(total=Coalesce(Sum('monto'), 0))['total']
            retiros = q.filter(aportacion=False).aggregate(total=Coalesce(Sum('monto'), 0))['total']
            balance = aports - retiros
            if monto > balance:
                raise serializers.ValidationError({'monto': f'No se puede hacer un retiro mayor al saldo actual: ${balance}'})

        fecha_entrega = data.get('fecha_entrega')
        tipo_de_movimiento = data.get('tipo_de_movimiento')
        today = date.today()
        if (tipo_de_movimiento == Movimiento.EFECTIVO and
                (fecha_entrega.year != today.year or
                 fecha_entrega.month != today.month)):
            raise serializers.ValidationError({"fecha_entrega": "Las aportaciones en efectivo sólo pueden ser del mes en curso."})

        return data


class MovimientoConcSerializer(serializers.ModelSerializer):
    nombre_socio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movimiento
        fields = ['id', 'nombre_socio', 'fecha_entrega', 'monto', 'aportacion',
                  'tipo_de_movimiento', 'fecha_banco', 'referencia_banco',
                  'proceso'
                  ]

    def get_nombre_socio(self, object):
        return object.clave_socio.nombres_apellidos()


class MovimientoPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = ['id', 'tipo_de_movimiento', 'fecha_banco', 'referencia_banco']


class MovimientoSingleSerializer(serializers.ModelSerializer):
    nombre_socio = serializers.SerializerMethodField(read_only=True)
    autor = serializers.StringRelatedField(read_only=True)
    proceso = serializers.SerializerMethodField(read_only=True)
    tipo_de_movimiento = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movimiento
        fields = '__all__'

    def get_proceso(self, object):
        return object.get_proceso_display()

    def get_tipo_de_movimiento(self, object):
        return object.get_tipo_de_movimiento_display()

    def get_nombre_socio(self, object):
        return object.clave_socio.nombres_apellidos()
