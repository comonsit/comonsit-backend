from rest_framework import serializers
from .models import Pago
# from contratos.models import ContratoCredito
from contratos.utility import deuda_calculator


class PagoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pago
        fields = "__all__"

    def validate(self, data):
        credito = data.get('credito')
        # TODO: is this check already done automatically?
        # """
        # check credito exists
        # """
        # if not ContratoCredito.objects.filter(folio=credito_id).exists():
        #     raise serializers.ValidationError({"credito": "Crédito inexistente."})
        #
        # TODO: should these checks be done in utility?
        # """
        # check credito is not already paid.
        # """
        # credito = ContratoCredito.objects.get(folio=credito_id)
        # if credito.estatus != ContratoCredito.DEUDA_PENDIENTE:
        #     raise serializers.ValidationError({"credito": "Este crédito ya está pagado"})
        fecha_pago = data.get('fecha_pago')
        deuda = deuda_calculator(credito, fecha_pago)
        if not deuda:
            # TODO: Should we give specific reasons for fail?
            raise serializers.ValidationError({"credito": "Este crédito no tiene deuda"})

        """
        check ammount does not exceed debt
        """
        cantidad = data.get('cantidad')
        # substitute for final debt calculator (same in interest check!!!)
        if cantidad > deuda.total:
            raise serializers.ValidationError({"monto": "El pago es mayor que la deuda"})

        """
        check interest payment within range
        """
        interes_ord = data.get('interes_ord')
        # TODO: update per date calculator
        if interes_ord > deuda.interes_ordinario:
            raise serializers.ValidationError({"interes_ord": "El pago es mayor a lo que se debe de interés ordinario"})

        """
        check interest payment within range
        """
        interes_mor = data.get('interes_mor')
        # TODO: update per date calculator
        if interes_mor > deuda.interes_moratorio:
            raise serializers.ValidationError({"interes_mor": "El pago es mayor a lo que se debe de interés moratorio"})

        """
        check interest payment less than total payment
        """
        # TODO: update per date calculator
        if interes_ord > cantidad:
            raise serializers.ValidationError({"interes_ord": "El pago de interés no puede ser mayor a lo que se está pagando"})

        return data
