from django.db import models


class Acopios(models.Model):
    CAFE = 'CF'
    MIEL = 'MI'
    JABON = 'JA'
    SUELDOS = 'SL'
    PRODUCTO_CHOICES = [
        (CAFE, 'Cafe'),
        (MIEL, 'Miel'),
        (JABON, 'Jabon'),
        (SUELDOS, 'Sueldos'),
    ]

    id = models.AutoField(primary_key=True)  # TODO: Público
    # claveSocio = models.ForeignKey(Users.claveSocio, on_delete=models.CASCADE, blank=False)  # TODO: on delete?
    fecha = models.DateField(auto_now_add=True)  # TODO: NO usar como timespamp?
    ingreso = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    kilos_de_producto = models.IntegerField(blank=True, null=True)  # TODO: meter límites máximo y mínimo?
    tipo_de_producto = models.CharField(max_length=2, choices=PRODUCTO_CHOICES, blank=True)
