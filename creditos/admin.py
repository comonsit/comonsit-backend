from django.contrib import admin
from .models import SolicitudCredito


class SolicitudCreditoAdmin(admin.ModelAdmin):
    model = SolicitudCredito


admin.site.register(SolicitudCredito, SolicitudCreditoAdmin)
