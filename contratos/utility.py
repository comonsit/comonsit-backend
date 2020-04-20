from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from rest_framework.serializers import ValidationError
from .models import ContratoCredito
from pagos.models import Pago


def deuda_calculator(credito, fecha=date.today()):
    if (not credito.fecha_inicio or
            credito.estatus_ejecucion != ContratoCredito.COBRADO or
            credito.estatus != ContratoCredito.DEUDA_PENDIENTE):
        return None
    if fecha < credito.fecha_inicio:
        raise ValidationError("La fecha es previa al inicio del Crédito")

    pagos = Pago.objects.filter(credito=credito).order_by('-fecha_pago')
    ultimo_pago = pagos[0] if pagos else None

    capital_pagado = pagos.aggregate(Sum('abono_capital'))['abono_capital__sum']
    capital_pagado = capital_pagado if capital_pagado else 0

    if credito.tipo_tasa == ContratoCredito.FIJA:
        # CAPITAL (calculated over original ammount, or pending ammount)
        capital_pendiente = credito.monto

        # INTERES ORDINARIO
        meses_transcurridos = relativedelta(fecha, credito.fecha_inicio).months
        interes_ordinario = capital_pendiente*(credito.tasa/100)*meses_transcurridos

        # INTERES MORATORIO
        plazo_total = credito.plazo + credito.prorroga
        tasa_moratoria = credito.tasa_moratoria if fecha > credito.fecha_vencimiento() else 0
        interes_moratorio = capital_pendiente*(tasa_moratoria/100)*(meses_transcurridos-plazo_total)

    elif credito.tipo_tasa == ContratoCredito.VARIABLE:
        # CAPITAL (calculated over original ammount, or pending ammount)
        capital_pendiente = credito.monto - capital_pagado

        # INTERES ORDINARIO
        fecha_ultimo_pago = credito.fecha_inicio
        interes_ord_acumulado = 0
        interes_mor_acumulado = 0
        if ultimo_pago:
            fecha_ultimo_pago = ultimo_pago.fecha_pago
            interes_ord_acumulado = ultimo_pago.deuda_prev_int_ord - ultimo_pago.interes_ord
            interes_mor_acumulado = ultimo_pago.deuda_prev_int_mor - ultimo_pago.interes_mor

        dias_transcurridos = relativedelta(fecha, fecha_ultimo_pago).days
        tasa_diaria = credito.tasa*12/365
        interes_ordinario = capital_pendiente*(tasa_diaria/100)*dias_transcurridos + interes_ord_acumulado

        # INTERES MORATORIO
        plazo_total_dias = relativedelta(credito.fecha_vencimiento(), credito.fecha_inicio).days
        tasa_moratoria_diaria = credito.tasa_moratoria*12/365 if fecha > credito.fecha_vencimiento() else 0
        interes_moratorio = capital_pendiente*Decimal(tasa_moratoria_diaria/100)*Decimal(dias_transcurridos-plazo_total_dias) + interes_mor_acumulado

    return {
            'total': credito.monto - capital_pagado + interes_ordinario + interes_moratorio,
            'interes_ordinario': interes_ordinario,
            'interes_moratorio': interes_moratorio,
            }
