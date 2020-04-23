from datetime import date
from rest_framework import serializers
from .models import Pago
from contratos.models import ContratoCredito
from contratos.utility import deuda_calculator


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = "__all__"
        extra_kwargs = {
            'interes_ord': {'read_only': True},
            'interes_mor': {'read_only': True},
            'abono_capital': {'read_only': True},
            'estatus_actual': {'read_only': True},
            'autor': {'read_only': True},
            'deuda_prev_total': {'read_only': True},
            'deuda_prev_int_ord': {'read_only': True},
            'deuda_prev_int_mor': {'read_only': True},
            }

    def validate(self, data):
        credito = data.get('credito')
        # TODO: reduntant check with utility?
        """
        check credito is not already paid.
        """
        if credito.estatus != ContratoCredito.DEUDA_PENDIENTE:
            raise serializers.ValidationError({"credito": f'Este crédito está {credito.get_estatus_display()}'})

        """
        Check if credit has been executed
        """
        if credito.estatus_ejecucion != ContratoCredito.COBRADO:
            raise serializers.ValidationError({"credito": f'Este crédito está {credito.get_estatus_ejecucion_display()}'})

        """
        Check Fecha pago within range
        """
        fecha_pago = data.get('fecha_pago')
        if fecha_pago > date.today():
            raise serializers.ValidationError({"fecha_pago": "La fecha de pago no puede ser mayor a hoy"})
        if fecha_pago < credito.fecha_inicio:
            raise serializers.ValidationError({"fecha_pago": "La fecha de pago no puede ser menor a la fecha de inicio del crédito."})

        """
        Check credit is payable
        """
        deuda = deuda_calculator(credito, fecha_pago)
        if not deuda:
            raise serializers.ValidationError({"credito": "Este crédito no tiene deuda"})

        """
        check ammount does not exceed debt
        """
        cantidad = data.get('cantidad')
        # substitute for final debt calculator (same in interest check!!!)
        if cantidad > deuda['total']:
            raise serializers.ValidationError({"monto": "El pago es mayor que la deuda"})
        return data

    def create(self, validated_data):
        current_user = self.context['request'].user
        credito = validated_data.pop('credito', None)
        fecha_pago = validated_data.pop('fecha_pago', None)
        deuda = deuda_calculator(credito, fecha_pago)
        cantidad = validated_data.pop('cantidad', None)
        abono_capital = cantidad
        interes_mor = 0
        if deuda['interes_moratorio'] > 0:
            if abono_capital > deuda['interes_moratorio']:
                interes_mor = deuda['interes_moratorio']
            else:
                interes_mor = abono_capital
            abono_capital -= interes_mor
        interes_ord = 0
        if deuda['interes_ordinario'] > 0:
            if abono_capital > deuda['interes_ordinario']:
                interes_ord = deuda['interes_ordinario']
            else:
                interes_ord = abono_capital
            abono_capital -= interes_ord

        # Unnecessary?
        if cantidad != (abono_capital + interes_ord + interes_mor):
            raise serializers.ValidationError({"cantidad": "Algo falló en el desglose de cantidad"})

        pago = Pago.objects.create(
                credito=credito,
                fecha_pago=fecha_pago,
                cantidad=cantidad,
                autor=current_user,
                interes_ord=interes_ord,
                interes_mor=interes_mor,
                abono_capital=abono_capital,
                estatus_actual=credito.get_validity(),
                deuda_prev_total=deuda['total'],
                deuda_prev_int_ord=deuda['interes_ordinario'],
                deuda_prev_int_mor=deuda['interes_moratorio'],
                **validated_data)

        # Check if payment is complete and change status
        if deuda['total'] == cantidad:
            credito.estatus = ContratoCredito.PAGADO
            credito.save()
        return pago


class PagoListSerializer(serializers.ModelSerializer):
    nombres = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pago
        fields = ['folio', 'credito', 'fecha_pago', 'nombres', 'region', 'cantidad']

    def get_nombres(self, object):
        return object.credito.clave_socio.nombres + ' ' + object.credito.clave_socio.apellido_paterno \
                + ' ' + object.credito.clave_socio.apellido_materno

    def get_region(self, object):
        return object.credito.clave_socio.comunidad.region.id
