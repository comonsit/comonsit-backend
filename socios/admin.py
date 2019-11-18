from django.contrib import admin
from .models import Socios


class SociosAdmin(admin.ModelAdmin):
    model = Socios


admin.site.register(Socios, SociosAdmin)
