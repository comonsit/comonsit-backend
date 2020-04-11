from django.db import models
from comonSitDjango.constants import PROCESOS


class SubCuenta(models.Model):
    nombre_cuenta = models.CharField(max_length=40, blank=False)
    proceso = models.CharField(max_length=2, choices=PROCESOS, blank=True, null=True)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_cuenta)


class ConceptoBanco(models.Model):
    nombre_concepto = models.CharField(max_length=40, blank=False)
    ingreso = models.BooleanField()  # True=Ingreso False=Egreso

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_concepto)


class MovimientoBanco(models.Model):
    referencia_banco = models.CharField(max_length=20, blank=False, unique=True)
    fecha = models.DateField(blank=False)
    concepto = models.ForeignKey(ConceptoBanco, on_delete=models.CASCADE, blank=False, related_name='movimiento_banco')
    sub_cuenta = models.ForeignKey(SubCuenta, on_delete=models.CASCADE, blank=False, related_name='movimiento_banco')
    referencia = models.CharField(max_length=60)
