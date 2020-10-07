from django.db import models


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

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_de_region)

    class Meta:
        verbose_name_plural = "Regiones"


class Comunidad(models.Model):
    nombre_de_comunidad = models.CharField(max_length=40, blank=False)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    ermita = models.ForeignKey('ermitas.Ermita', on_delete=models.SET_NULL, null=True, blank=True)
    inegi_extra = models.ForeignKey('ermitas.InegiLocalidad', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{nombre}".format(nombre=self.nombre_de_comunidad)

    class Meta:
        verbose_name_plural = "Comunidades"


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
