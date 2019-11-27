from django.db import models


class Socios(models.Model):
    PRODUCTOR = 'PR'
    TRABAJADOR = 'TR'
    PROD_TRAB_CHOICES = [
        (PRODUCTOR, 'Productor'),
        (TRABAJADOR, 'Trabajador'),
    ]
    ACTIVO = 'AC'
    NO_PARTICIPA = 'NP'
    BAJA = 'BA'
    ESTATUS_CHOICES = [
        (ACTIVO, 'Activo'),
        (NO_PARTICIPA, 'No Participa'),
        (BAJA, 'Baja'),
    ]

    clave_socio = models.CharField(max_length=10, primary_key=True)  # TODO: RESTRICCIONES!
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    comunidad = models.ForeignKey('tsumbalil.Comunidades', on_delete=models.SET_NULL, null=True, blank=True)
    # region = models.ForeignKey('tsumbalil.Regiones', on_delete=models.SET_NULL, null=True, blank=True)
    curp = models.CharField(max_length=18, verbose_name='CURP', blank=True)  # TODO: Revisar Restricciones, homoclave?
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    fecha_ingr_yomol_atel = models.DateField()
    fecha_ingr_programa = models.DateField()
    cargo = models.ForeignKey('tsumbalil.Cargos', on_delete=models.SET_NULL, null=True, blank=True)
    prod_trab = models.CharField(max_length=2, choices=PROD_TRAB_CHOICES, blank=False)
    clave_anterior = models.CharField(max_length=10, blank=True, null=True)
    estatus_cafe = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_miel = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_yip = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_gral = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    # foto = models.imageField()

    def __str__(self):
        return '{0}: {1} {2}'.format(self.clave_socio, self.nombres, self.apellidos)
