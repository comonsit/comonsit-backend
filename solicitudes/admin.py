from django.contrib import admin
from .models import SolicitudCredito, ChatSolicitudCredito


class SolicitudCreditoAdmin(admin.ModelAdmin):
    model = SolicitudCredito


class ChatSolicitudCreditoAdmin(admin.ModelAdmin):
    model = ChatSolicitudCredito
    list_display = ("solicitud",)


admin.site.register(SolicitudCredito, SolicitudCreditoAdmin)
admin.site.register(ChatSolicitudCredito, ChatSolicitudCreditoAdmin)
