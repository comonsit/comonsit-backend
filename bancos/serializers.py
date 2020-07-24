from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
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
    fecha = serializers.SerializerMethodField(read_only=True)
    subcuenta_id_cont = serializers.SerializerMethodField(read_only=True)
    subcuenta_nombre = serializers.SerializerMethodField(read_only=True)
    saldo = serializers.SerializerMethodField(read_only=True)
    referencia = serializers.SerializerMethodField(read_only=True)
    # ingresos = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)
    # egresos = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)

    class Meta:
        model = RegistroContable
        fields = [
            'id', 'fecha', 'subcuenta_id_cont', 'subcuenta_nombre',
            'referencia', 'cantidad', 'ingr_egr', 'saldo'
            ]

    def get_fecha(self, object):
        return object.movimiento_banco.fecha

    def get_subcuenta_id_cont(self, object):
        return object.subcuenta.id_contable

    def get_subcuenta_nombre(self, object):
        return object.subcuenta.nombre

    def get_referencia(self, object):
        nombre = None
        if object.aport_retiro:
            tipo = 'Aportación' if object.aport_retiro.aportacion else 'Retiro'
            nombre = object.aport_retiro.clave_socio.nombres + ' ' + \
                object.aport_retiro.clave_socio.apellido_paterno + ' ' + \
                object.aport_retiro.clave_socio.apellido_materno

        elif object.pago:
            tipo = 'Pago'
            nombre = object.pago.credito.clave_socio.nombres + ' ' + \
                object.pago.credito.clave_socio.apellido_paterno + ' ' + \
                object.pago.credito.clave_socio.apellido_materno
        elif object.ej_credito:
            tipo = 'Ejecución Crédito'
            nombre = object.ej_credito.clave_socio.nombres + ' ' + \
                object.ej_credito.clave_socio.apellido_paterno + ' ' + \
                object.ej_credito.clave_socio.apellido_materno

        if nombre:
            return f'{tipo} - {nombre}'
        else:
            # TODO: incluir la nota
            return '- - -'

    def get_saldo(self, object):
        q = RegistroContable.objects.filter(movimiento_banco__fecha__lte=object.movimiento_banco.fecha)
        # ingresos = q.filter(ingr_egr=True).aggregate(tot=Sum('cantidad'))['tot']
        # egresos = q.filter(ingr_egr=False).aggregate(tot=Coalesce(Sum('cantidad'), 0))['tot']
        # ingresos = ingresos if ingresos else 0
        # egresos = egresos if egresos else 0
        saldos = q.aggregate(
            ingresos=Coalesce(Sum('cantidad', filter=Q(ingr_egr=True)), 0),
            egresos=Coalesce(Sum('cantidad', filter=Q(ingr_egr=False)), 0)
            )
        return {
            **saldos,
            'total': saldos['ingresos'] - saldos['egresos']
        }


class MovimientoBancoSerializer(serializers.ModelSerializer):
    selectedItems = serializers.ListField(child=serializers.IntegerField(), allow_empty=True, write_only=True)
    dataType = serializers.CharField(max_length=20, min_length=4, allow_blank=False, write_only=True)
    ingrEgr = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = MovimientoBanco
        fields = "__all__"

    def validate(self, data):
        """
        Check General type of Movement
        """
        dataType = data.get('dataType')
        # TODO: CHANGE FOR NON MAGIC WORDS!!
        if dataType not in ["Movimientos", "Pagos", "EjCredito", "Otros"]:
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
        # TODO:
        """
        if "OTROS" check that subcuenta is not part of system subcuenta, inside subcuentas.py
        """
        # TODO:
        """
        Check for valid bank?
        """
        # TODO:
        """
        Check that selectedItems has at least length 1, and strictly length 1 for "Otros"
        """
        # TODO:
        """
        if "otros" than ingr_egr is REQUIRED, and must match subcuenta VALId options.
        """
        # TODO:
        """
        La referencia bancaria SOLO en mayúsculas!
        """
        return data

    def create(self, validated_data):
        data_type = validated_data.pop('dataType')
        selected_items = validated_data.pop('selectedItems')
        cantidad = validated_data.get('cantidad')
        ingr_egr = validated_data.pop('ingrEgr', None)

        instance = MovimientoBanco.objects.create(**validated_data)

        if data_type == "Movimientos":
            for movimiento in selected_items:
                mov = Movimiento.objects.get(id=movimiento)
                subcuenta_id = subcuentas.get_type_aport(mov)
                subcuenta = SubCuenta.objects.get(id=subcuenta_id)
                RegistroContable.objects.create(
                    subcuenta=subcuenta,
                    movimiento_banco=instance,
                    aport_retiro=mov,
                    cantidad=cantidad,
                    ingr_egr=mov.aportacion
                )

        elif data_type == "Pagos":
            for pago_id in selected_items:
                pago = Pago.objects.get(pk=pago_id)
                # CAPITAL
                if pago.abono_capital and pago.abono_capital > 0:
                    subcuenta_id = subcuentas.get_type_pago(pago)
                    subcuenta = SubCuenta.objects.get(id=subcuenta_id)
                    RegistroContable.objects.create(
                        subcuenta=subcuenta,
                        movimiento_banco=instance,
                        pago=pago,
                        cantidad=pago.abono_capital,
                        ingr_egr=True
                    )
                # INTERÉSES ORDINARIOS
                if pago.interes_ord and pago.interes_ord > 0:
                    subcuenta = SubCuenta.objects.get(id=subcuentas.INGR_INT_ORD)
                    RegistroContable.objects.create(
                        subcuenta=subcuenta,
                        movimiento_banco=instance,
                        pago=pago,
                        cantidad=pago.interes_ord,
                        ingr_egr=True
                    )
                # INTERÉSES MORATORIOS
                if pago.interes_mor and pago.interes_mor > 0:
                    subcuenta = SubCuenta.objects.get(id=subcuentas.INGR_INT_MOR)
                    RegistroContable.objects.create(
                        subcuenta=subcuenta,
                        movimiento_banco=instance,
                        pago=pago,
                        cantidad=pago.interes_mor,
                        ingr_egr=True
                    )

        elif data_type == "EjCredito":
            for credito_id in selected_items:
                credito = ContratoCredito.objects.get(pk=credito_id)
                subcuenta_id = subcuentas.get_type_credito(credito)
                subcuenta = SubCuenta.objects.get(id=subcuenta_id)
                RegistroContable.objects.create(
                    subcuenta=subcuenta,
                    movimiento_banco=instance,
                    ej_credito=credito,
                    cantidad=cantidad,
                    ingr_egr=False
                )

        elif data_type == "Otros":
            subc = SubCuenta.objects.get(id=selected_items[0])
            RegistroContable.objects.create(
                subcuenta=subc,
                movimiento_banco=instance,
                cantidad=cantidad,
                ingr_egr=ingr_egr
            )

        return instance
