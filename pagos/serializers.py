from datetime import date
from rest_framework import serializers
from .models import Pago, Condonacion
from contratos.models import ContratoCredito
from contratos.utility import deuda_calculator


class PagoSerializer(serializers.ModelSerializer):
    estatus_nuevo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pago
        fields = "__all__"
        extra_kwargs = {
            'estatus_previo': {'read_only': True},
            'autor': {'read_only': True},
            'deuda_prev_total': {'read_only': True},
            'deuda_prev_capital': {'read_only': True},
            'deuda_prev_int_ord': {'read_only': True},
            'deuda_prev_int_mor': {'read_only': True}
            }

    def validate(self, data):
        credito = data.get('credito')
        # TODO: reduntant check with utility?
        """
        check credito is not already paid.
        """
        if credito.estatus != ContratoCredito.DEUDA_PENDIENTE:
            raise serializers.ValidationError({
                "credito": f'Este crédito está {credito.get_estatus_display()}'})

        """
        Check if credit has been executed
        """
        if credito.estatus_ejecucion != ContratoCredito.COBRADO:
            raise serializers.ValidationError({
                "credito": f'Este crédito está {credito.get_estatus_ejecucion_display()}'})

        """
        Check Fecha pago within range
        """
        fecha_pago = data.get('fecha_pago')
        if fecha_pago > date.today():
            raise serializers.ValidationError({
                "fecha_pago": "La fecha de pago no puede ser mayor a hoy"})

        """
        Check the payment date is after start of credit
        """
        if fecha_pago < credito.fecha_inicio:
            raise serializers.ValidationError({
                "fecha_pago": "La fecha de pago no puede ser menor a la fecha de inicio del crédito."})

        """
        Check the payment date is after all previously registered payments
        """
        previous_payments = Pago.objects.filter(credito=credito).order_by('-fecha_pago')
        if previous_payments:
            latest_payment_date = previous_payments[0].fecha_pago
            if fecha_pago < latest_payment_date:
                formatted_date = latest_payment_date.strftime('%d %b %Y')
                raise serializers.ValidationError({
                    "fecha_pago": f'La fecha de pago no puede ser menor al último pago generado ({formatted_date})',
                    "non_field_errors": ""})

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
            raise serializers.ValidationError({
                "cantidad": f"La cantidad {cantidad} del pago no puede ser mayor que la deuda {deuda['total_deuda']}"})

        interes_ord = data.get('interes_ord')
        if interes_ord > deuda['interes_ordinario_deuda']:
            raise serializers.ValidationError({
                "interes_ord": f"El pago de interes ordinario {interes_ord} es mayor"
                               f" a lo que se debe de interés ordinario {deuda['interes_ordinario_deuda']}"})

        interes_mor = data.get('interes_mor')
        if interes_mor > deuda['interes_moratorio_deuda']:
            raise serializers.ValidationError({
                "interes_mor": f"El pago {interes_mor} es mayor a"
                               f" lo que se debe de interés moratorio {deuda['interes_moratorio_deuda']}"})

        abono_capital = data.get('abono_capital')
        if abono_capital > deuda['capital_por_pagar']:
            raise serializers.ValidationError({
                "abono_capital": f"El pago {abono_capital} es mayor a lo que se debe de capital {deuda['capital_por_pagar']}"})

        """
        Check quantities match
        """
        if cantidad != abono_capital + interes_mor + interes_ord:
            raise serializers.ValidationError({
                "cantidad": "Las cantidades a abonar no son equivalentes a la cantidad total"})
        return data

    def create(self, validated_data):
        current_user = self.context['request'].user
        credito = validated_data.get('credito', None)
        fecha_pago = validated_data.get('fecha_pago', None)
        deuda = deuda_calculator(credito, fecha_pago)
        cantidad = validated_data.get('cantidad', None)

        pago = Pago.objects.create(autor=current_user,
                                   estatus_previo=credito.get_status(fecha_pago),
                                   deuda_prev_total=deuda['total_deuda'],
                                   deuda_prev_capital=deuda['capital_por_pagar'],
                                   deuda_prev_int_ord=deuda['interes_ordinario_deuda'],
                                   deuda_prev_int_mor=deuda['interes_moratorio_deuda'],
                                   **validated_data)

        # Check if payment is complete and change status
        if pago and deuda['total_deuda'] == cantidad:
            credito.estatus = ContratoCredito.PAGADO
            credito.fecha_final = fecha_pago
            credito.save()
        return pago

    def get_estatus_nuevo(self, object):
        if object.fecha_pago:
            return object.credito.get_status(object.fecha_pago)
        return object.credito.get_status()


class PagoPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'fecha_banco', 'referencia_banco']


class PagoListSerializer(serializers.ModelSerializer):
    nombres = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pago
        fields = ['id', 'credito', 'fecha_pago', 'nombres', 'region', 'cantidad',
                  'estatus_previo', 'fecha_banco', 'referencia_banco']

    def get_nombres(self, object):
        return object.credito.clave_socio.nombres_apellidos()

    def get_region(self, object):
        return object.credito.clave_socio.comunidad.region.id


class CondonacionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condonacion
        fields = "__all__"


class CondonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condonacion
        fields = ['credito', 'justificacion']

    def validate(self, data):
        credito = data.get('credito')
        # TODO: Next two checks are duplicated with PagoSerializer.validate
        """
        check credito is not already paid.
        """
        if credito.estatus != ContratoCredito.DEUDA_PENDIENTE:
            raise serializers.ValidationError({
                "credito": f'Este crédito está {credito.get_estatus_display()}'})

        """
        Check if credit has been executed
        """
        if credito.estatus_ejecucion != ContratoCredito.COBRADO:
            raise serializers.ValidationError({
                "credito": f'Este crédito está {credito.get_estatus_ejecucion_display()}'})

        """
        Check if no capital is due
        """
        deuda = deuda_calculator(credito, date.today())
        if deuda['capital_por_pagar'] > 0:
            raise serializers.ValidationError({
                "credito": f"Sólo se pueden condonar créditos sin capital pendiente por pagar."
                           f"Este crédito tiene {deuda['capital_por_pagar']} de capital pendiente."})

    def create(self, validated_data):
        current_user = self.context['request'].user
        credito = validated_data.get('credito', None)
        justificacion = validated_data.get('justificacion', None)
        deuda = deuda_calculator(credito, date.today())

        condonacion = Condonacion.objects.create(credito=credito,
                                                 fecha_condonacion=date.today(),
                                                 autor=current_user,
                                                 cantidad=deuda['total_deuda'],
                                                 interes_ord=deuda['interes_ordinario_deuda'],
                                                 interes_mor=deuda['interes_moratorio_deuda'],
                                                 estatus_previo=credito.get_status(date.today()),
                                                 justificacion=justificacion)

        # Credit is automatically set as payed
        credito.estatus = ContratoCredito.CONDONADO
        credito.fecha_final = date.today()
        credito.save()

        return condonacion
