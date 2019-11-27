from django.contrib import admin
from .models import Socio


class SocioAdmin(admin.ModelAdmin):
    model = Socio


admin.site.register(Socio, SocioAdmin)
