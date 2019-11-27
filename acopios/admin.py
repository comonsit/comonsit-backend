from django.contrib import admin
from .models import Acopio


class AcopioAdmin(admin.ModelAdmin):
    model = Acopio


admin.site.register(Acopio, AcopioAdmin)
