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
    # TODO: duplicated with acopios, centralize in single place
    CAFE = 'CF'
    MIEL = 'MI'
    JABON = 'JA'
    SUELDOS = 'SL'
    PROCESO_CHOICES = [
        (CAFE, 'Cafe'),
        (MIEL, 'Miel'),
        (JABON, 'Jabon'),
        (SUELDOS, 'Sueldos'),
    ]
    id = models.AutoField(primary_key=True)
    clave_socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, blank=False, related_name='movimiento')
    fecha_entrega = models.DateField()
    monto = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    proceso = models.CharField(max_length=2, choices=PROCESO_CHOICES, default='CF')
    aportacion = models.BooleanField(blank=False, default=True)  # false = retiro
    tipo_de_movimiento = models.CharField(max_length=2, choices=MOVIMIENTO_CHOICES, blank=True)
    responsable_entrega = models.CharField(max_length=50, blank=True)
    fecha_banco = models.DateField(blank=True, null=True)
    referencia_banco = models.CharField(max_length=20, blank=True, null=True)
    autor = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, related_name='movimiento_autor')

    def __str__(self):
        if self.aportacion:
            return 'Socio: {0} ${1}   {2}'.format(self.clave_socio, self.monto, self.fecha_entrega)
        return 'Socio: {0} -${1}    {2}'.format(self.clave_socio, self.monto, self.fecha_entrega)
