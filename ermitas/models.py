from django.contrib.gis.db import models

class Interzona(models.Model):
    interzona_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return "Interzona %d: %s" % (self.interzona_id, self.nombre)

class Zona(models.Model):
    zona_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    interzona = models.ForeignKey(Interzona, on_delete=models.CASCADE)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return "Zona %d: %s" % (self.zona_id, self.nombre)

class Municipio(models.Model):
    municipio_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return "Municipio %d: %s" % (self.municipio_id, self.nombre)

class Ermita(models.Model):
    ermita_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return "Ermita %d: %s" % (self.ermita_id, self.nombre)

class InegiLocalidad(models.Model):
    localidad_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    altitud = models.IntegerField()
    longitud = models.FloatField()
    latitud = models.FloatField()
    ubicacion = models.PointField(srid=4326)
