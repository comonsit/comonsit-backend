from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from rest_framework.serializers import ValidationError
from .models import ContratoCredito
from pagos.models import Pago


def deuda_calculator(credito, fecha):
    if (not credito.fecha_inicio or
            credito.estatus_ejecucion != ContratoCredito.COBRADO or
            credito.estatus != ContratoCredito.DEUDA_PENDIENTE):
        return {}
    if fecha < credito.fecha_inicio:
        raise ValidationError(f"La fecha {fecha.ctime()} es previa a {credito.fecha_inicio.ctime()} de {credito}")

    pagos = Pago.objects.filter(credito=credito).order_by('-fecha_pago')

    capital_pagado = pagos.aggregate(Sum('abono_capital'))['abono_capital__sum']
    capital_pagado = capital_pagado if capital_pagado else 0

    interes_ord_pagado = pagos.aggregate(Sum('interes_ord'))['interes_ord__sum']
    interes_ord_pagado = interes_ord_pagado if interes_ord_pagado else 0

    interes_mor_pagado = pagos.aggregate(Sum('interes_mor'))['interes_mor__sum']
    interes_mor_pagado = interes_mor_pagado if interes_mor_pagado else 0

    if credito.tipo_tasa == ContratoCredito.FIJA:
        # CAPITAL (calculated over original ammount, or pending ammount)
        monto_original = credito.monto

        # INTERES ORDINARIO
        delta = relativedelta(fecha, credito.fecha_inicio)
        meses_transcurridos = delta.years*12 + delta.months
        interes_ordinario = monto_original*(credito.tasa/100)*meses_transcurridos

        # INTERES MORATORIO
        plazo_total = credito.plazo + credito.prorroga
        tasa_moratoria = credito.tasa_moratoria if fecha > credito.fecha_vencimiento() else 0
        interes_moratorio = monto_original*Decimal(tasa_moratoria/100)*(meses_transcurridos-plazo_total)

    elif credito.tipo_tasa == ContratoCredito.VARIABLE:
        # CAPITAL (calculated over original ammount, or pending ammount)
        capital_pendiente = credito.monto - capital_pagado

        # INTERES ORDINARIO
        fecha_ultimo_pago = credito.fecha_inicio
        interes_ord_acumulado = 0
        interes_mor_acumulado = 0
        if pagos:
            ultimo_pago = pagos[0]
            fecha_ultimo_pago = ultimo_pago.fecha_pago
            interes_ord_acumulado = ultimo_pago.deuda_prev_int_ord
            interes_mor_acumulado = ultimo_pago.deuda_prev_int_mor
            if fecha < fecha_ultimo_pago:
                raise ValidationError(f"La fecha {fecha.ctime()} es previa al último pago #{ultimo_pago.folio}")

        dias_transcurridos = fecha - fecha_ultimo_pago
        tasa_diaria = credito.tasa*12/365
        interes_ordinario = (capital_pendiente*Decimal(tasa_diaria/100)*dias_transcurridos.days
                             + interes_ord_acumulado)

        # INTERES MORATORIO
        plazo_total_dias = credito.fecha_vencimiento() - credito.fecha_inicio
        dias_vencido = (dias_transcurridos.days-plazo_total_dias.days)
        tasa_moratoria_diaria = credito.tasa_moratoria*12/365 if fecha > credito.fecha_vencimiento() else 0
        interes_moratorio = (capital_pendiente*Decimal(tasa_moratoria_diaria/100)*dias_vencido
                             + interes_mor_acumulado)

    cantidad_pagada = pagos.aggregate(Sum('cantidad'))['cantidad__sum']
    cantidad_pagada = cantidad_pagada if cantidad_pagada else 0

    return {
            'total_deuda': credito.monto - cantidad_pagada + interes_ordinario + interes_moratorio,
            'monto_original': credito.monto,
            'capital_abonado': capital_pagado,
            'capital_por_pagar': credito.monto - capital_pagado,
            'interes_ordinario_abonado': interes_ord_pagado,
            'interes_ordinario_total': interes_ordinario,
            'interes_ordinario_deuda': interes_ordinario - interes_ord_pagado,
            'interes_moratorio_abonado': interes_mor_pagado,
            'interes_moratorio_total': interes_moratorio,
            'interes_moratorio_deuda': interes_moratorio - interes_mor_pagado,
            'fecha': fecha
            }
