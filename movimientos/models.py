from django.db import models
from comonSitDjango.constants import PROCESOS


class Movimiento(models.Model):
    EFECTIVO = 'EF'
    BANCOS = 'BA'
    TRANSFERENCIA = 'TR'
    MOVIMIENTO_CHOICES = [
        (EFECTIVO, 'Efectivo'),
        (BANCOS, 'Bancos'),
        (TRANSFERENCIA, 'Transferencia')
    ]
    id = models.AutoField(primary_key=True)
    clave_socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, blank=False, related_name='movimiento')
    fecha_entrega = models.DateField()
    monto = models.DecimalField(max_digits=9, decimal_places=2, blank=False)
    proceso = models.CharField(max_length=2, choices=PROCESOS, default='CF')
    aportacion = models.BooleanField(blank=False, default=True)  # false = retiro
    tipo_de_movimiento = models.CharField(max_length=2, choices=MOVIMIENTO_CHOICES, blank=True)
    responsable_entrega = models.CharField(max_length=50, blank=True)
    fecha_banco = models.DateField(blank=True, null=True)
    referencia_banco = models.CharField(max_length=20, blank=True, null=True)
    referencia_banco_id = models.ForeignKey('bancos.MovimientoBanco', on_delete=models.CASCADE, blank=True, null=True, related_name='movimiento')
    autor = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, related_name='movimiento_autor')

    def __str__(self):
        if self.aportacion:
            return 'Socio: {0} ${1}   {2}'.format(self.clave_socio, self.monto, self.fecha_entrega)
        return 'Socio: {0} -${1}    {2}'.format(self.clave_socio, self.monto, self.fecha_entrega)
