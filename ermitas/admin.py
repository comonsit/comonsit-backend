from django.contrib import admin
from .models import Ermita, Zona, Municipio, Interzona, InegiLocalidad


class ErmitaAdmin(admin.ModelAdmin):
    model = Ermita

class ZonaAdmin(admin.ModelAdmin):
    model = Zona

class MunicipioAdmin(admin.ModelAdmin):
    model = Municipio

class InterzonaAdmin(admin.ModelAdmin):
    model = Interzona

class InegiLocalidadAdmin(admin.ModelAdmin):
    model = InegiLocalidad

admin.site.register(Ermita, ErmitaAdmin)
admin.site.register(Zona, ZonaAdmin)
admin.site.register(Interzona, InterzonaAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(InegiLocalidad, InegiLocalidadAdmin)
