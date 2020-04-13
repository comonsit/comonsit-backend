from django.db import models


class Pago(models.Model):
    folio = models.AutoField(primary_key=True)
    credito = models.ForeignKey('contratos.ContratoCredito', on_delete=models.CASCADE, blank=False, related_name='pago')
    fecha_pago = models.DateField(blank=False)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    fecha_banco = models.DateField(blank=True, null=True)
    referencia_banco = models.CharField(max_length=20, blank=True, null=True)
    autor = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, related_name='pago_autor')
    interes_ord = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    interes_mor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
