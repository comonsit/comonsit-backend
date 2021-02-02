from django.contrib.gis.db import models


class Interzona(models.Model):
    interzona_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return "%d: %s" % (self.interzona_id, self.nombre)


class Zona(models.Model):
    zona_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    interzona = models.ForeignKey(Interzona, on_delete=models.CASCADE)
    poly = models.MultiPolygonField(srid=4326, blank=False, null=True, default=None)
    poly_encuesta = models.MultiPolygonField(srid=4326, blank=False, null=True, default=None)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f'{self.nombre} ({self.zona_id})'


class Municipio(models.Model):
    municipio_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f'{self.nombre} ({self.municipio_id})'


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
        verbose_name = "INEGI localidad"
        verbose_name_plural = "INEGI localidades"

    def __str__(self):
        return "InegiLocalidad %s in %s" % (self.nombre, str(self.municipio))


class Ermita(models.Model):
    ermita_id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)

    # a possible link to an INEGI Localidad. A match is not always possible
    # and sometimes they are a little complicated, so we give an option
    # for a human-readable comment about the quality of the match as well
    localidad = models.ForeignKey(InegiLocalidad,
                                  on_delete=models.CASCADE,
                                  null=True, blank=True)
    localidad_nota = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return "Ermita %d: %s" % (self.ermita_id, self.nombre)
