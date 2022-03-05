from rest_framework import serializers
from contratos.models import ContratoCredito
from comonSitDjango.constants import SUELDOS

#
# EJECUCIÓN DE CRÉDITOS
#
EJ_CRED_PROD = 2
EJ_CRED_TRAB = 4
INGR_INT_ORD = 25
INGR_INT_MOR = 26
EJ_CRED_PROD_FONDO_COMUN = 35

def get_type_credito(credito):
    if credito.fondo_comun:
        return EJ_CRED_PROD_FONDO_COMUN
    if credito.solicitud.proceso != SUELDOS:
        return EJ_CRED_PROD
    return EJ_CRED_TRAB


#
# PAGOS
#
PAGO_VIGENTE_PROD = 3
PAGO_VIGENTE_TRAB = 5
PAGO_VENCIDO_PROD = 6
PAGO_VENCIDO_TRAB = 7
PAGO_CAPITAL_FONDO_COMUN = 36

SET_VIGENTES = {PAGO_VIGENTE_PROD, PAGO_VIGENTE_TRAB}
SET_PAGO_PROD = {PAGO_VIGENTE_PROD, PAGO_VENCIDO_PROD}


def get_type_pago(pago):
    filt_set = {
        PAGO_VIGENTE_PROD, PAGO_VENCIDO_PROD, PAGO_VIGENTE_TRAB, PAGO_VENCIDO_TRAB
        }
    if pago.credito.fondo_comun:
        return PAGO_CAPITAL_FONDO_COMUN

    if pago.estatus_previo == ContratoCredito.VIGENTE:
        filt_set = filt_set & SET_VIGENTES
    else:
        filt_set = filt_set - SET_VIGENTES

    if pago.credito.solicitud.proceso != SUELDOS:
        filt_set = filt_set & SET_PAGO_PROD
    else:
        filt_set = filt_set - SET_PAGO_PROD
    if len(filt_set) != 1:
        raise serializers.ValidationError("Algo falló al verificar el tipo de pago")
    else:
        # Get single item of filtered set
        return next(iter(filt_set))


#
# APORTACIONES Y RETIROS
#
APORT_ORD_PROD = 17
RETIRO_ORD_PROD = 18
APORT_ORD_TRAB = 19
RETIRO_ORD_TRAB = 20
APORT_EXC_PROD = 21
RETIRO_EXC_PROD = 22
APORT_EXC_TRAB = 23
RETIRO_EXC_TRAB = 24

SET_ALL_APORT_RET = {
    APORT_ORD_PROD, RETIRO_ORD_PROD, APORT_ORD_TRAB, RETIRO_ORD_TRAB,
    APORT_EXC_PROD, RETIRO_EXC_PROD, APORT_EXC_TRAB, RETIRO_EXC_TRAB
    }
SET_APORTACIONES = {
    APORT_ORD_PROD, APORT_ORD_TRAB, APORT_EXC_PROD, APORT_EXC_TRAB
    }
SET_ORDINARIAS = {
    APORT_ORD_PROD, RETIRO_ORD_PROD, APORT_ORD_TRAB, RETIRO_ORD_TRAB
    }
SET_PRODUCTORES = {
    APORT_ORD_PROD, RETIRO_ORD_PROD, APORT_EXC_PROD, RETIRO_EXC_PROD
    }


def get_type_aport(movimiento):
    filtered_set = {
        APORT_ORD_PROD, RETIRO_ORD_PROD, APORT_ORD_TRAB, RETIRO_ORD_TRAB,
        APORT_EXC_PROD, RETIRO_EXC_PROD, APORT_EXC_TRAB, RETIRO_EXC_TRAB
        }
    if movimiento.aportacion:
        filtered_set = filtered_set & SET_APORTACIONES
    else:
        filtered_set = SET_ALL_APORT_RET - SET_APORTACIONES

    if movimiento.ordinario:
        filtered_set = filtered_set & SET_ORDINARIAS
    else:
        filtered_set = filtered_set - SET_ORDINARIAS

    if movimiento.proceso != SUELDOS:
        filtered_set = filtered_set & SET_PRODUCTORES
    else:
        filtered_set = filtered_set - SET_PRODUCTORES
    if len(filtered_set) != 1:
        raise serializers.ValidationError("Algo falló al verificar el tipo de aportación/retiro")
    else:
        # Get single item of filtered set
        return next(iter(filtered_set))
