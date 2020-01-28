from django.contrib import admin
from .models import Movimiento


class MovimientoAdmin(admin.ModelAdmin):
    model = Movimiento


admin.site.register(Movimiento, MovimientoAdmin)
