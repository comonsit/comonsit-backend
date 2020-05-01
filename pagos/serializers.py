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
        check ammounts do not exceed debt
        """
        cantidad = data.get('cantidad')
        # substitute for final debt calculator (same in interest check!!!)
        if cantidad > deuda['total_deuda']:
            raise serializers.ValidationError({"monto": "El pago es mayor que la deuda"})

        interes_ord = data.get('interes_ord')
        if interes_ord > deuda['interes_ordinario_deuda']:
            raise serializers.ValidationError({"interes_ord": "El pago es mayor a lo que se debe de interés ordinario"})

        interes_mor = data.get('interes_mor')
        if interes_mor > deuda['interes_moratorio_deuda']:
            raise serializers.ValidationError({"interes_mor": "El pago es mayor a lo que se debe de interés moratorio"})

        abono_capital = data.get('abono_capital')
        if abono_capital > deuda['capital_por_pagar']:
            raise serializers.ValidationError({"abono_pendiente": "El pago es mayor a lo que se debe de capital"})

        """
        Check quantities match
        """
        if cantidad != abono_capital + interes_mor + interes_ord:
            raise serializers.ValidationError({"cantidad": "Las cantidades a abonar no son equivalentes a la cantidad total"})
        return data

    def create(self, validated_data):
        current_user = self.context['request'].user
        credito = validated_data.get('credito', None)
        fecha_pago = validated_data.get('fecha_pago', None)
        deuda = deuda_calculator(credito, fecha_pago)
        cantidad = validated_data.get('cantidad', None)

        pago = Pago.objects.create(
                autor=current_user,
                estatus_actual=credito.get_validity(),
                deuda_prev_total=deuda['total_deuda'],
                deuda_prev_int_ord=deuda['interes_ordinario_deuda'],
                deuda_prev_int_mor=deuda['interes_moratorio_deuda'],
                **validated_data)

        # Check if payment is complete and change status
        if pago and deuda['total_deuda'] == cantidad:
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
