from django.db import models


class ContratoCredito(models.Model):

    DEUDA_PENDIENTE = 'DP'  # VENCIDO / VIGENTE
    PAGADO = 'PA'
    ESTATUS_CHOICES = [
        (DEUDA_PENDIENTE, 'Deuda Pendiente'),
        (PAGADO, 'Pagado')
    ]

    COBRADO = 'CO'
    POR_COBRAR = 'PC'
    CANCELADO = 'CA'
    ESTATUS_EJE_CHOICES = [
        (COBRADO, 'Cobrado'),
        (POR_COBRAR, 'Por cobrar'),
        (CANCELADO, 'Cancelado')
    ]

    folio = models.AutoField(primary_key=True)
    solicitud = models.OneToOneField('solicitudes.SolicitudCredito', on_delete=models.CASCADE, blank=False, related_name='contrato')
    clave_socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, blank=False, related_name='contrato')
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    monto = models.DecimalField(max_digits=9, decimal_places=2, blank=False)
    plazo = models.PositiveSmallIntegerField(blank=False)  # number of months
    tasa = models.DecimalField(max_digits=7, decimal_places=4, blank=False)
    prorroga = models.PositiveSmallIntegerField(blank=False, default=0)  # number of months
    estatus = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    referencia_banco = models.CharField(max_length=20, blank=True, null=True)
    fecha_salida_banco = models.DateField(blank=True, null=True)
    estatus_ejecucion = models.CharField(max_length=2, choices=ESTATUS_EJE_CHOICES, blank=False)

    def __str__(self):
        return '{0}- ({1}) ${2}'.format(self.folio, self.clave_socio, self.estatus)
