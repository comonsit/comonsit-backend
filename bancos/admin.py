from django.contrib import admin
from .models import Banco, SubCuenta, MovimientoBanco, RegistroContable


class BancoAdmin(admin.ModelAdmin):
    model = SubCuenta
    list_display = ("nombre_cuenta", "nombre_banco")


class SubCuentaAdmin(admin.ModelAdmin):
    model = SubCuenta
    list_display = ("nombre", "id_contable", "tipo")


class MovimientoBancoAdmin(admin.ModelAdmin):
    model = MovimientoBanco
    list_display = ("referencia_banco", "fecha", "cantidad")


class RegistroContableAdmin(admin.ModelAdmin):
    model = MovimientoBanco
    list_display = ("subcuenta", "cantidad")


admin.site.register(Banco, BancoAdmin)
admin.site.register(SubCuenta, SubCuentaAdmin)
admin.site.register(MovimientoBanco, MovimientoBancoAdmin)
admin.site.register(RegistroContable, RegistroContableAdmin)
