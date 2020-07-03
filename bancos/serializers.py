from rest_framework import serializers
from contratos.models import ContratoCredito
from movimientos.models import Movimiento
from pagos.models import Pago
from .models import Banco, SubCuenta, MovimientoBanco, RegistroContable
from . import subcuentas


class BancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banco
        fields = "__all__"


class SubCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCuenta
        fields = "__all__"


class RegistroContableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContable
        fields = "__all__"


class MovimientoBancoSerializer(serializers.ModelSerializer):
    # TODO: change for banco ID or serializer?
    banco = serializers.IntegerField(write_only=True)
    selectedItems = serializers.ListField(child=serializers.IntegerField(), allow_empty=True, write_only=True)
    dataType = serializers.CharField(max_length=20, min_length=4, allow_blank=False, write_only=True)

    class Meta:
        model = MovimientoBanco
        fields = "__all__"

    def validate(self, data):
        """
        Check General type of Movement
        """
        dataType = data.get('dataType')
        # TODO: CHANGE FOR NON MAGIC WORDS!!
        if dataType not in ["Movimientos", "Pagos", "EjCreditos", "Otros"]:
            raise serializers.ValidationError({"dataType": f'Error inesperado, movimiento no válido.'})
        # TODO:
        """
        Check that acopios exist and have not been linked
        """
        # TODO:
        """
        Check that pagos exist and have not been linked
        """
        # TODO:
        """
        Check that ej_créditos exist and have not been linked
        """
        # TODO:
        """
        Check that ammounts add correctly
        """
        """
        Check for valid bank?
        """
        return data

    def create(self, validated_data):
        banco = validated_data.pop('banco')
        data_type = validated_data.pop('dataType')
        selected_items = validated_data.pop('selectedItems')
        cantidad = validated_data.get('cantidad')

        instance = MovimientoBanco.objects.create(**validated_data)

        if data_type == "Movimientos":
            for movimiento in selected_items:
                mov = Movimiento.objects.get(id=movimiento)
                subcuenta_id = subcuentas.APORT if mov.aportacion else subcuentas.RETIRO
                subcuenta = SubCuenta.objects.get(id=subcuenta_id)
                RegistroContable.objects.create(
                    subcuenta=subcuenta,
                    movimiento_banco=instance,
                    aport_retiro=mov,
                    cantidad=cantidad,
                    ingr_egr=mov.aportacion
                )

        # elif data_type == "Pagos":
        #     for pago_id in selected_items:
        #         pago = Pago.objects.get(pk=pago_id)
        #         ref = f"Pago de {pago.credito.clave_socio.nombres}"
        #         RegistroContable.objects.create(
        #             subcuenta=3,  # TODO: AVOID MAGIC NUMBERS!
        #             movimiento_banco=instance,
        #             pago=pago,
        #             referencia=ref,
        #             cantidad=cantidad,
        #             ingr_egr=True
        #         )
        #
        # elif data_type == "EjCredito":
        #     for credito_id in selected_items:
        #         credito = ContratoCredito.objects.get(pk=credito_id)
        #         RegistroContable.objects.create(
        #             subcuenta=subcuentas.EJ_CRED,
        #             movimiento_banco=instance,
        #             ej_credito=credito,
        #             cantidad=cantidad,
        #             ingr_egr=False
        #         )
        # elif data_type == "Otros":
        #     subc = SubCuenta.objects.get(id=selected_items[0])
        #     ingreso = subc.tipo == SubCuenta.INGRESO  # TODO: consider INGRESO/EGRESO CASE!!!
        #     RegistroContable.objects.create(
        #         subcuenta=subc,  # TODO: AVOID MAGIC NUMBERS!
        #         movimiento_banco=instance,
        #         ej_credito=credito,
        #         referencia=subc.nombre,
        #         cantidad=cantidad,
        #         ingr_egr=ingreso
        #     )

        return instance
