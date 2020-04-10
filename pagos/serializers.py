from rest_framework import serializers
from .models import Pago
from contratos.models import ContratoCredito


class PagoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pago
        fields = "__all__"

    def validate(self, data):
        credito = data.get('credito')
        # """
        # check credito exists
        # """
        # if not ContratoCredito.objects.filter(folio=credito_id).exists():
        #     raise serializers.ValidationError({"credito": "Crédito inexistente."})
        #
        # """
        # check credito is not already paid.
        # """
        # credito = ContratoCredito.objects.get(folio=credito_id)
        if credito.estatus != ContratoCredito.DEUDA_PENDIENTE:
            raise serializers.ValidationError({"credito": "Este crédito ya está pagado"})

        """
        check ammount does not exceed debt
        """
        cantidad = data.get('cantidad')
        # substitute for final debt calculator (same in interest check!!!)
        if cantidad > (credito.monto + credito.monto*(credito.tasa/100)*credito.plazo):
            raise serializers.ValidationError({"monto": "El pago es mayor que la deuda"})

        """
        check interest payment within range
        """
        interes_ord = data.get('interes_ord')
        # TODO: update per date calculator
        if interes_ord > (credito.monto*(credito.tasa/100)*credito.plazo):
            raise serializers.ValidationError({"interes_ord": "El pago de interés es mayor que lo que se debe"})

        """
        check interest payment less than total payment
        """
        # TODO: update per date calculator
        if interes_ord > cantidad:
            raise serializers.ValidationError({"interes_ord": "El pago de interés no puede ser mayor a lo que se está pagando"})

        return data
