from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework.serializers import ValidationError
from .models import ContratoCredito


def deuda_calculator(credito, fecha=date.today()):
    if (not credito.fecha_inicio or
            credito.estatus_ejecucion != ContratoCredito.COBRADO or
            credito.estatus != ContratoCredito.DEUDA_PENDIENTE):
        return None

    # To make date "aware" and comparable with Django DateTime
    if fecha < credito.fecha_inicio:
        raise ValidationError("La fecha es previa al inicio del Crédito")

    meses_transcurridos = relativedelta(fecha, credito.fecha_inicio).months
    interes_ordinario = credito.monto*(credito.tasa/100)*meses_transcurridos

    plazo_total = credito.plazo + credito.prorroga
    interes_moratorio = 0
    if fecha > credito.fecha_vencimiento():
        interes_moratorio = credito.monto*(credito.tasa/100)*(meses_transcurridos-plazo_total)

    return {
            'total': credito.monto + interes_ordinario + interes_moratorio,
            'interes_ordinario': interes_ordinario,
            'interes_moratorio': interes_moratorio,
            }
