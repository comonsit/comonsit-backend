from django.contrib import admin
from .models import Cargos, Comunidades, Regiones


class CargosAdmin(admin.ModelAdmin):
    model = Cargos
    list_display = ("nombre_de_cargo",)


class RegionesAdmin(admin.ModelAdmin):
    model = Regiones
    list_display = ("nombre_de_region",)


class ComunidadesAdmin(admin.ModelAdmin):
    model = Comunidades
    list_display = ("nombre_de_comunidad", "region")


admin.site.register(Cargos, CargosAdmin)
admin.site.register(Regiones, RegionesAdmin)
admin.site.register(Comunidades, ComunidadesAdmin)
