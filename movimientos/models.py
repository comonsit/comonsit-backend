from django.db import models


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
    monto = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    empresa = models.ForeignKey('tsumbalil.Empresa', on_delete=models.CASCADE, default=1)  # 1 = Ts'umbal
    fecha_banco = models.DateField()
    aportacion = models.BooleanField(blank=False, default=True)  # false = retiro
    tipo_de_movimiento = models.CharField(max_length=2, choices=MOVIMIENTO_CHOICES, blank=True)

    def __str__(self):
        if self.aportacion:
            return 'Socio: {0} ${1}   {2}'.format(self.clave_socio, self.monto, self.fecha_entrega)
        return 'Socio: {0} -${1}    {2}'.format(self.clave_socio, self.monto, self.fecha_entrega)
