from django.db import models
from comonSitDjango.constants import PROCESOS


class Acopio(models.Model):
    id = models.AutoField(primary_key=True)  # TODO: Público
    clave_socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, blank=False, related_name='acopio') # TODO: on delete?
    fecha = models.DateField()  # TODO: NO usar como timespamp?
    ingreso = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    kilos_de_producto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # TODO: meter límites máximo y mínimo?
    tipo_de_producto = models.CharField(max_length=2, choices=PROCESOS, blank=True)

    def __str__(self):
        return '{0}: ${1}'.format(self.id, self.ingreso)
