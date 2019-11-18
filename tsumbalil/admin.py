from django.contrib import admin
from .models import Cargos, Comunidades, Regiones


class CargosAdmin(admin.ModelAdmin):
    model = Cargos


class ComunidadesAdmin(admin.ModelAdmin):
    model = Comunidades


class RegionesAdmin(admin.ModelAdmin):
    model = Regiones


admin.site.register(Cargos, CargosAdmin)
admin.site.register(Comunidades, ComunidadesAdmin)
admin.site.register(Regiones, RegionesAdmin)
