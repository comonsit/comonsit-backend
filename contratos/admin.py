from django.contrib import admin
from .models import ContratoCredito


class ContratoCreditoAdmin(admin.ModelAdmin):
    model = ContratoCredito


admin.site.register(ContratoCredito, ContratoCreditoAdmin)
