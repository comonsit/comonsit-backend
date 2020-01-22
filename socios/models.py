from django.db import models


class Socio(models.Model):
    ACTIVO = 'AC'
    NO_PARTICIPA = 'NP'
    BAJA = 'BA'
    ESTATUS_CHOICES = [
        (ACTIVO, 'Activo'),
        (NO_PARTICIPA, 'No Participa'),
        (BAJA, 'Baja'),
    ]

    clave_socio = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    comunidad = models.ForeignKey('tsumbalil.Comunidad', on_delete=models.SET_NULL, null=True, blank=True)
    curp = models.CharField(max_length=18, verbose_name='CURP', blank=True)  # TODO: Revisar Restricciones, homoclave?
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    fecha_ingr_yomol_atel = models.DateField()
    fecha_ingr_programa = models.DateField()
    cargo = models.ForeignKey('tsumbalil.Cargo', on_delete=models.SET_NULL, null=True, blank=True)
    cargo_coop = models.ForeignKey('tsumbalil.CargoCoop', on_delete=models.CASCADE, default=1)  # 1 = Ninguno
    empresa = models.ForeignKey('tsumbalil.Empresa', on_delete=models.CASCADE, default=1)  # 1 = Ts'umbal
    productor = models.BooleanField(blank=False, default=False)
    trabajador = models.BooleanField(blank=False, default=False)
    clave_anterior = models.CharField(max_length=10, blank=True, null=True)
    estatus_cafe = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_miel = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_yip = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_gral = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    # foto = models.imageField()

    def __str__(self):
        return '{0}: {1} {2}'.format(self.clave_socio, self.nombres, self.apellidos)
