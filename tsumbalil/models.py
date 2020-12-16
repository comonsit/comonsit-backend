from django.contrib.gis.db import models


class Cargo(models.Model):
    nombre_de_cargo = models.CharField(max_length=40, blank=False)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_de_cargo)


class CargoCoop(models.Model):
    nombre_cargo_coop = models.CharField(max_length=40, blank=False)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_cargo_coop)


class Region(models.Model):
    nombre_de_region = models.CharField(max_length=40, blank=False)
    poly = models.PolygonField(srid=4326, blank=False, null=True, default=None)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_de_region)

    class Meta:
        verbose_name_plural = "Regiones"


def get_region_sin_asignar():
    region_sin_asignar, _ = Region.objects.get_or_create(id=20, nombre_de_region="Sin asignar")
    return region_sin_asignar.pk


class Comunidad(models.Model):
    nombre_de_comunidad = models.CharField(max_length=50, blank=False)
    region = models.ForeignKey(Region,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               default=get_region_sin_asignar)
    ermita = models.ForeignKey('ermitas.Ermita',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    inegi_extra = models.ForeignKey('ermitas.InegiLocalidad',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_de_comunidad)

    class Meta:
        verbose_name_plural = "Comunidades"
        unique_together = ('nombre_de_comunidad', 'region',)


class Empresa(models.Model):
    nombre_empresa = models.CharField(max_length=40, blank=False)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_empresa)


class Puesto_Trabajo(models.Model):
    puesto = models.CharField(max_length=40, blank=False)

    def __str__(self):
        return "{puesto}".format(puesto=self.puesto)


class Fuente(models.Model):
    fuente = models.CharField(max_length=40, blank=False)

    def __str__(self):
        return "{fuente}".format(fuente=self.fuente)
