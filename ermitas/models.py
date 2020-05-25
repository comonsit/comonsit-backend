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
    localidad_id = models.IntegerField(primary_key=True)

    # this is the INEGI clave, which is not unique across municipios
    clave = models.IntegerField(default=0)
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    altitud = models.IntegerField(default=0)
    poblacion = models.IntegerField(default=0)

    # 4326 is Point(x,y) = Longitude,Latitude format
    ubicacion = models.PointField(srid=4326)
    ubicacion.geography = True

    class Meta:
        # sort by municipio and then by nombre
        ordering = ["municipio", "nombre"]

    def __str__(self):
        return "InegiLocalidad %s in %s" % (self.nombre, str(self.municipio))
