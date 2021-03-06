from django.db import models
from tsumbalil.models import CargoCoop
from comonSitDjango.constants import ESTATUS_CHOICES


class Socio(models.Model):

    MASCULINO = 'MA'
    FEMENINO = 'FE'
    OTRO = 'OT'
    GENERO_CHOICES = [
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
        (OTRO, 'Otro')
    ]

    clave_socio = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, null=True, blank=True)
    comunidad = models.ForeignKey('tsumbalil.Comunidad', on_delete=models.CASCADE)
    curp = models.CharField(max_length=18, verbose_name='CURP', blank=True)  # TODO: Revisar Restricciones, homoclave?
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_ingr_yomol_atel = models.DateField(blank=True, null=True)
    fecha_ingr_programa = models.DateField(blank=True, null=True)
    cargo = models.ForeignKey('tsumbalil.Cargo', on_delete=models.SET_NULL, null=True, blank=True)
    cargo_coop = models.ManyToManyField(CargoCoop,
                                        related_name='Socio_cargo_coop',
                                        blank=True,
                                        default=1)  # 1 = Ninguno
    empresa = models.ForeignKey('tsumbalil.Empresa', on_delete=models.CASCADE, null=True, default=None)
    puesto = models.ForeignKey('tsumbalil.Puesto_Trabajo',
                               on_delete=models.CASCADE,
                               related_name='Socio_puesto',
                               null=True)
    fuente = models.ForeignKey('tsumbalil.Fuente',
                               on_delete=models.CASCADE,
                               related_name='Socio_fuente',
                               null=True)
    clave_anterior = models.CharField(max_length=10, blank=True, null=True)
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES, blank=False)
    estatus_cafe = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_miel = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_yip = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_trabajador = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_comonSit = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    doc_curp = models.BooleanField(blank=False, default=False)
    doc_act_nac = models.BooleanField(blank=False, default=False)
    doc_ine = models.BooleanField(blank=False, default=False)
    doc_domicilio = models.BooleanField(blank=False, default=False)
    doc_rfc = models.BooleanField(blank=False, default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # foto = models.imageField()

    def __str__(self):
        return '{0}: {1} {2} {3}'.format(self.clave_socio, self.nombres, self.apellido_paterno, self.apellido_materno)

    def nombres_apellidos(self):
        if self.apellido_materno:
            return self.nombres + ' ' + self.apellido_paterno + ' ' + self.apellido_materno
        return self.nombres + ' ' + self.apellido_paterno
