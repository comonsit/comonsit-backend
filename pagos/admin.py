from django.contrib import admin
from .models import Pago


class PagoAdmin(admin.ModelAdmin):
    model = Pago


admin.site.register(Pago, PagoAdmin)
