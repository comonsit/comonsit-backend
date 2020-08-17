from django.db import models


class Banco(models.Model):
    nombre_banco = models.CharField(max_length=40, blank=False)
    nombre_cuenta = models.CharField(max_length=40, blank=False)
    numero_cuenta = models.CharField(max_length=100, blank=False)
    clabe = models.CharField(max_length=18, blank=True)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_cuenta)


class SubCuenta(models.Model):
    INGRESO = 'IN'
    EGRESO = 'EG'
    INGRESO_EGRESO = 'IE'
    TIPO_MOV_CHOICES = [
        (INGRESO, 'Ingreso'),
        (EGRESO, 'Egreso'),
        (INGRESO_EGRESO, 'Ingreso/Egreso')
    ]

    nombre = models.CharField(max_length=60, blank=False)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, blank=False, related_name='subcuenta')
    id_contable = models.CharField(max_length=40, blank=False)
    tipo = models.CharField(max_length=2, choices=TIPO_MOV_CHOICES, blank=False)
    sistema = models.BooleanField(blank=True, default=True)  # False are those not linked to the system

    def __str__(self):
        return "{id_cont} {nombre}".format(id_cont=self.id_contable, nombre=self.nombre)


class MovimientoBanco(models.Model):
    referencia_banco = models.CharField(max_length=20, blank=False, unique=True)
    fecha = models.DateField(blank=False)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    referencia_alf = models.CharField(max_length=60, blank=True, null=True)
    fecha_auto = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, related_name='movimiento_banco')


class RegistroContable(models.Model):
    subcuenta = models.ForeignKey(SubCuenta, on_delete=models.CASCADE, blank=False)
    movimiento_banco = models.ForeignKey(MovimientoBanco, on_delete=models.CASCADE, blank=False)
    aport_retiro = models.ForeignKey('movimientos.movimiento', on_delete=models.CASCADE, blank=True, null=True)
    pago = models.ForeignKey('pagos.pago', on_delete=models.CASCADE, blank=True, null=True)
    ej_credito = models.ForeignKey('contratos.contratocredito', on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    ingr_egr = models.BooleanField(blank=False, default=True)  # ingr = True // egr = False
