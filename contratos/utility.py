from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from rest_framework.serializers import ValidationError
from .models import ContratoCredito


def deuda_calculator(credito, fecha=datetime.today()):
    if (not credito.fecha_inicio or
            credito.estatus_ejecucion != ContratoCredito.COBRADO or
            credito.estatus != ContratoCredito.DEUDA_PENDIENTE):
        return None

    # To make datetime "aware" and comparable with Django DateTime
    utc = pytz.UTC
    fecha = fecha.replace(tzinfo=utc)
    if fecha < credito.fecha_inicio:
        raise ValidationError("La fecha es previa al inicio del Crédito")

    meses_transcurridos = relativedelta(fecha, credito.fecha_inicio).months
    interes_ordinario = credito.monto*(credito.tasa/100)*meses_transcurridos
    interes_moratorio = 0
    prorroga = credito.prorroga if credito.prorroga else 0  # TODO: substitute by a default 0 in create of model?
    plazo_total = credito.plazo + prorroga
    fecha_vencimiento = credito.fecha_inicio + relativedelta(months=+plazo_total)
    if fecha > fecha_vencimiento:
        interes_moratorio = credito.monto*(credito.tasa/100)*(meses_transcurridos-plazo_total)

    return {
            'total': credito.monto + interes_ordinario + interes_moratorio,
            'interes_ordinario': interes_ordinario,
            'interes_moratorio': interes_moratorio,
            }
