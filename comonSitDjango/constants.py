CAFE = 'CF'
MIEL = 'MI'
JABON = 'JA'
SUELDOS = 'SL'

PROCESOS = [
    (CAFE, 'Café'),
    (MIEL, 'Miel'),
    (JABON, 'Jabon'),
    (SUELDOS, 'Sueldos'),
]

# TODO: Move to a general access
PROCESOS_FIELDS = {
    'CF': 'estatus_cafe',
    'MI': 'estatus_miel',
    'JA': 'estatus_yip',
    'SL': 'estatus_trabajador'
}

ACTIVO = 'AC'
NO_PARTICIPA = 'NP'
BAJA = 'BA'
ESTATUS_CHOICES = [
    (ACTIVO, 'Activo'),
    (NO_PARTICIPA, 'No Participa'),
    (BAJA, 'Baja'),
]
