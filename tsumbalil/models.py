from django.db import models


class Cargos(models.Model):
    nombre_de_cargo = models.CharField(max_length=40, blank=False)


class Regiones(models.Model):
    nombre_de_region = models.CharField(max_length=40, blank=False)


class Comunidades(models.Model):
    nombre_de_comunidad = models.CharField(max_length=40, blank=False)
    region = models.ForeignKey(Regiones, on_delete=models.SET_NULL, null=True, blank=True)
