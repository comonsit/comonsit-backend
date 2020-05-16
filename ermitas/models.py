from django.db import models
from comonSitDjango.constants import PROCESOS

class Interzona(models.Model):
    interzona_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

class Zona(models.Model):
    zona_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    interzona = models.ForeignKey(Interzona, on_delete=models.CASCADE)

class Municipio(models.Model):
    municipio_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

class Ermita(models.Model):
    ermita_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)

class InegiLocalidad(models.Model):
    localidad_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    altitud = models.IntegerField()
    longitud = models.FloatField()
    latitud = models.FloatField()
