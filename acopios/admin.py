from django.contrib import admin
from .models import Acopios


class AcopiosAdmin(admin.ModelAdmin):
    model = Acopios


admin.site.register(Acopios, AcopiosAdmin)
