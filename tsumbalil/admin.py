from django.contrib import admin
from .models import Cargo, CargoCoop, Comunidad, Region, Empresa, \
                    Puesto_Trabajo, Fuente, SubCuenta


class CargoAdmin(admin.ModelAdmin):
    model = Cargo
    list_display = ("nombre_de_cargo",)


class CargoCoopAdmin(admin.ModelAdmin):
    model = CargoCoop
    list_display = ("nombre_cargo_coop",)


class RegionAdmin(admin.ModelAdmin):
    model = Region
    list_display = ("nombre_de_region",)


class ComunidadAdmin(admin.ModelAdmin):
    model = Comunidad
    list_display = ("nombre_de_comunidad", "region")


class EmpresaAdmin(admin.ModelAdmin):
    model = Empresa
    list_display = ("nombre_empresa",)


class PuestoAdmin(admin.ModelAdmin):
    model = Puesto_Trabajo
    list_display = ("puesto",)


class FuenteAdmin(admin.ModelAdmin):
    model = Fuente
    list_display = ("fuente",)


class SubCuentaAdmin(admin.ModelAdmin):
    model = SubCuenta
    list_display = ("nombre_cuenta",)


admin.site.register(Cargo, CargoAdmin)
admin.site.register(CargoCoop, CargoCoopAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Comunidad, ComunidadAdmin)
admin.site.register(Puesto_Trabajo, PuestoAdmin)
admin.site.register(Fuente, FuenteAdmin)
admin.site.register(SubCuenta, SubCuentaAdmin)
