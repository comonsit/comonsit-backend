from django.db import models


class ContratoCredito(models.Model):

    EN_CURSO = 'EC'
    RETRASO = 'RE'
    CANCELADO = 'CA'
    ESTATUS_CHOICES = [
        (EN_CURSO, 'En curso'),
        (RETRASO, 'Retraso'),
        (CANCELADO, 'Cancelado')
    ]

    COBRADO = 'CO'
    POR_COBRAR = 'PC'
    CANCELADO = 'CA'
    ESTATUS_EF_CHOICES = [
        (COBRADO, 'Cobrado'),
        (POR_COBRAR, 'Por cobrar'),
        (CANCELADO, 'Cancelado')
    ]

    REVISION = 'RV'
    ESTATUS_EJE_CHOICES = [
        (COBRADO, 'Cobrado'),
        (POR_COBRAR, 'Por cobrar'),
        (REVISION, 'Revisión')
    ]

    folio = models.AutoField(primary_key=True)
    solicitud = models.OneToOneField('solicitudes.SolicitudCredito', on_delete=models.CASCADE, blank=False, related_name='contrato')
    clave_socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, blank=False, related_name='contrato')
    promotor = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, related_name='contrato')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=9, decimal_places=2, blank=False)
    plazo = models.PositiveSmallIntegerField(blank=False)
    tasa = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    prorroga = models.DateField(blank=True, null=True)
    estatus = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    estatus_efectivo = models.CharField(max_length=2, choices=ESTATUS_EF_CHOICES, blank=False)
    fecha_salida_banco = models.DateTimeField(blank=True, null=True)
    estatus_ejecucion = models.CharField(max_length=2, choices=ESTATUS_EJE_CHOICES, blank=False)

    def __str__(self):
        return '{0}- ({1}) ${2}'.format(self.folio_solicitud, self.clave_socio, self.estatus)
