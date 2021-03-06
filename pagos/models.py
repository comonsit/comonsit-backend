from django.db import models
from contratos.models import ContratoCredito


class Pago(models.Model):
    ESTATUS_CHOICES = [
        (ContratoCredito.VIGENTE, 'Vigente'),
        (ContratoCredito.VENCIDO, 'Vencido'),
    ]

    credito = models.ForeignKey('contratos.ContratoCredito',
                                on_delete=models.CASCADE,
                                blank=False,
                                related_name='pago')
    fecha_pago = models.DateField(blank=False)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    fecha_banco = models.DateField(blank=True, null=True)
    referencia_banco = models.CharField(max_length=20, blank=True, null=True)
    autor = models.ForeignKey('users.User',
                              on_delete=models.CASCADE,
                              blank=False,
                              related_name='pago_autor')
    interes_ord = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    interes_mor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    abono_capital = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    estatus_previo = models.CharField(max_length=2, choices=ESTATUS_CHOICES, blank=False)
    deuda_prev_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    deuda_prev_capital = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    deuda_prev_int_ord = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    deuda_prev_int_mor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


class Condonacion(models.Model):
    credito = models.OneToOneField('contratos.ContratoCredito',
                                   on_delete=models.CASCADE,
                                   blank=False,
                                   related_name='condonacion')
    fecha_condonacion = models.DateField(blank=False)
    autor = models.ForeignKey('users.User',
                              on_delete=models.CASCADE,
                              blank=False,
                              related_name='condonacion_autor')
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    interes_ord = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    interes_mor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    estatus_previo = models.CharField(max_length=2, choices=Pago.ESTATUS_CHOICES, blank=False)
    justificacion = models.CharField(max_length=100)
