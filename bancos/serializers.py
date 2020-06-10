from rest_framework import serializers
from movimientos.serializers import MovimientoSerializer
from pagos.serializers import PagoListSerializer
from .models import Banco, SubCuenta, MovimientoBanco, RegistroContable


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
    movs = MovimientoSerializer(many=True)
    pags = PagoListSerializer(many=True)
    # TODO: Check if we can use with non existing registries
    # others = RegistroContableSerializer(many=True)

    class Meta:
        model = MovimientoBanco
        fields = "__all__"
        extra_kwargs = {
            'movs': {'write_only': True},
            'pags': {'write_only': True},
            # 'others': {'write_only': True},
            }

    def validate(self, data):
        # TODO:
        """
        Check that acopios have not been linked
        """
        # TODO:
        """
        Check that pagos have not been linked
        """
        # TODO:
        """
        Check that ammounts add correctly
        """
        return data

    def create(self, validated_data):
        movs_data = validated_data.pop('movs')
        pags_data = validated_data.pop('pags')
        # others_data = validated_data.pop('others')

        instance = MovimientoBanco.objects.create(**validated_data)

        for mv in movs_data:
            print(mv)
            # mv.referencia_banco_id = instance
            # socio_nombre = mv.clave_socio.nombres + ' ' + mv.clave_socio.apellido_paterno + ' ' + mv.clave_socio.apellido_materno
            # # TODO: update Movimientos SUBCUENTA
            # # TODO: remove magic number subcuenta
            # RegistroContable.objects.create(subcuenta=2, movimiento_banco=instance,
            #                                 aport_retiro=mv, referencia=socio_nombre,
            #                                 cantidad=mv.monto, ingr_egr=mv.aportacion)

        for pago in pags_data:
            print(pago)
            # TODO: update Movimientos SUBCUENTA
            # TODO: remove magic number subcuenta
            # pago.referencia_banco_id = instance
            # socio_nombre = pago.credito.clave_socio.nombres + ' ' + pago.credito.clave_socio.apellido_paterno + ' ' + pago.credito.clave_socio.apellido_materno
            # if pago.abono_capital > 0:
            #     RegistroContable.objects.create(subcuenta=3, movimiento_banco=instance,
            #                                     pago=pago, referencia=socio_nombre,
            #                                     cantidad=pago.abono_capital, ingr_egr=True)
            # if pago.interes_ord > 0:
            #     RegistroContable.objects.create(subcuenta=4, movimiento_banco=instance,
            #                                     pago=pago, referencia=socio_nombre,
            #                                     cantidad=pago.interes_ord, ingr_egr=True)
            # if pago.interes_mor > 0:
            #     RegistroContable.objects.create(subcuenta=5, movimiento_banco=instance,
            #                                     pago=pago, referencia=socio_nombre,
            #                                     cantidad=pago.interes_mor, ingr_egr=True)

        # for o_data in others_data:
        #     RegistroContable.objects.create(**o_data)

        return instance
