from decimal import Decimal, ROUND_DOWN
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from rest_framework.serializers import ValidationError
from .models import ContratoCredito
from pagos.models import Pago


def round_decimals_down(number):
    if type(number) in (int, float, Decimal):
        return Decimal(number).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    return number


def cleanup_dictionary(dictionary):
    for k, value in dictionary.items():
        if k != 'fecha':
            dictionary[k] = round_decimals_down(value)
    return dictionary


def deuda_calculator(credito, fecha, old_status=False):
    if not credito.fecha_inicio \
       or credito.estatus_ejecucion != ContratoCredito.COBRADO \
       or (credito.estatus != ContratoCredito.DEUDA_PENDIENTE and not old_status):
        return {}
    if fecha < credito.fecha_inicio:
        raise ValidationError({
            "non_field_errors": f"La fecha {fecha.strftime('%d %b %Y')} es previa al"
                                f" inicio del crédito {credito.fecha_inicio.strftime('%d %b %Y')}"})

    pagos = Pago.objects.filter(credito=credito, fecha_pago__lte=fecha).order_by('-fecha_pago')

    capital_pagado = pagos.aggregate(Sum('abono_capital'))['abono_capital__sum']
    capital_pagado = capital_pagado if capital_pagado else 0

    interes_ord_abonado = pagos.aggregate(Sum('interes_ord'))['interes_ord__sum']
    interes_ord_abonado = interes_ord_abonado if interes_ord_abonado else 0

    interes_mor_abonado = pagos.aggregate(Sum('interes_mor'))['interes_mor__sum']
    interes_mor_abonado = interes_mor_abonado if interes_mor_abonado else 0

    #
    # TASA FIJA
    #
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

        cantidad_pagada = pagos.aggregate(Sum('cantidad'))['cantidad__sum']
        cantidad_pagada = cantidad_pagada if cantidad_pagada else 0

        deuda_dictionary = {
            'total_deuda': credito.monto - cantidad_pagada + interes_ordinario + interes_moratorio,
            'monto_original': credito.monto,
            'capital_abonado': capital_pagado,
            'capital_por_pagar': (credito.monto - capital_pagado),
            'interes_ordinario_abonado': interes_ord_abonado,
            'interes_ordinario_total': interes_ordinario,
            'interes_ordinario_deuda': (interes_ordinario - interes_ord_abonado),
            'interes_moratorio_abonado': interes_mor_abonado,
            'interes_moratorio_total': interes_moratorio,
            'interes_moratorio_deuda': (interes_moratorio - interes_mor_abonado),
            'fecha': fecha
        }

        return cleanup_dictionary(deuda_dictionary)

    #
    # TASA VARIABLE
    #
    elif credito.tipo_tasa == ContratoCredito.VARIABLE:
        # CAPITAL for Variable is calculated over pending ammount
        # TODO: Verify if on original ammount
        capital_pendiente = credito.monto - capital_pagado

        # INTERES ORDINARIO
        fecha_ultimo_pago = credito.fecha_inicio
        interes_ord_parcial = 0
        interes_mor_parcial = 0
        if pagos:
            ultimo_pago = pagos[0]
            fecha_ultimo_pago = ultimo_pago.fecha_pago
            interes_ord_parcial = ultimo_pago.deuda_prev_int_ord - ultimo_pago.interes_ord
            interes_mor_parcial = ultimo_pago.deuda_prev_int_mor - ultimo_pago.interes_mor
            if fecha < fecha_ultimo_pago:
                raise ValidationError({
                    "non_field_errors": f"La fecha {fecha.ctime()} es previa al último pago #{ultimo_pago.folio}"})

        dias_transcurridos = fecha - fecha_ultimo_pago
        tasa_diaria = credito.tasa*12/365

        interes_ordinario = (capital_pendiente*Decimal(tasa_diaria/100)*dias_transcurridos.days
                             + interes_ord_parcial)

        # INTERES MORATORIO
        # Override days in debt for Moratorio
        if fecha_ultimo_pago < credito.fecha_vencimiento():
            dias_transcurridos = fecha - credito.fecha_vencimiento()

        tasa_moratoria_diaria = credito.tasa_moratoria*12/365 if fecha > credito.fecha_vencimiento() else 0

        interes_moratorio = (capital_pendiente*Decimal(tasa_moratoria_diaria/100)*dias_transcurridos.days
                             + interes_mor_parcial)

        deuda_dictionary = {
            'total_deuda': capital_pendiente + interes_ordinario + interes_moratorio,
            'monto_original': credito.monto,
            'capital_abonado': capital_pagado,
            'capital_por_pagar': (credito.monto - capital_pagado),
            'interes_ordinario_abonado': interes_ord_abonado,
            'interes_ordinario_total': None,  # TODO
            'interes_ordinario_deuda': interes_ordinario,
            'interes_moratorio_abonado': interes_mor_abonado,
            'interes_moratorio_total': None,
            'interes_moratorio_deuda': interes_moratorio,
            'fecha': fecha
        }

        return cleanup_dictionary(deuda_dictionary)
