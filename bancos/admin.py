from django.contrib import admin
from .models import ConceptoBanco, SubCuenta, MovimientoBanco


class SubCuentaAdmin(admin.ModelAdmin):
    model = SubCuenta
    list_display = ("nombre_cuenta",)


class ConceptoBancoAdmin(admin.ModelAdmin):
    model = ConceptoBanco
    list_display = ("nombre_concepto", "ingreso")


class MovimientoBancoAdmin(admin.ModelAdmin):
    model = MovimientoBanco


admin.site.register(SubCuenta, SubCuentaAdmin)
admin.site.register(ConceptoBanco, ConceptoBancoAdmin)
admin.site.register(MovimientoBanco, MovimientoBancoAdmin)
