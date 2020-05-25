from django.contrib.gis import admin
from .models import Ermita, Zona, Municipio, Interzona, InegiLocalidad

admin.site.register(Ermita)
admin.site.register(Zona)
admin.site.register(Interzona)
admin.site.register(Municipio)

class InegiLocalidadAdmin(admin.GeoModelAdmin):
    model = InegiLocalidad

admin.site.register(InegiLocalidad, InegiLocalidadAdmin)
