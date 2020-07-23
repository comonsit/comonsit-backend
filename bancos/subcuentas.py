from rest_framework import serializers
from comonSitDjango.constants import SUELDOS

EJ_CRED = 2
PAGO_CAPT_VIGENTE = 3
PAGO_CAPT_VENCIDO = 6

# APORTACIONES Y RETIROS
APORT_ORD_PROD = 17
RETIRO_ORD_PROD = 18
APORT_ORD_TRAB = 19
RETIRO_ORD_TRAB = 20
APORT_EXC_PROD = 21
RETIRO_EXC_PROD = 22
APORT_EXC_TRAB = 23
RETIRO_EXC_TRAB = 24

SET_ALL = {
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
    if movimiento.aportacion:
        filtered_set = SET_APORTACIONES
    else:
        filtered_set = SET_ALL - SET_APORTACIONES

    if movimiento.ordinario:
        filtered_set = filtered_set & SET_ORDINARIAS
    else:
        filtered_set = filtered_set - SET_ORDINARIAS

    if movimiento.proceso != SUELDOS:
        filtered_set = filtered_set & SET_PRODUCTORES
    else:
        filtered_set = filtered_set - SET_PRODUCTORES
    if len(filtered_set) != 1:
        serializers
        raise serializers.ValidationError("Algo falló al verificar el tipo de aportación/retiro")
    else:
        # Get single item of filtered set
        return next(iter(filtered_set))


INGR_INT_ORD = 25
INGR_INT_MOR = 26
