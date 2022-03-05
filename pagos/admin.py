from django.contrib import admin
from .models import Pago, Condonacion


class PagoAdmin(admin.ModelAdmin):
    model = Pago

class CondonacionAdmin(admin.ModelAdmin):
    model = Condonacion


admin.site.register(Pago, PagoAdmin)
admin.site.register(Condonacion, CondonacionAdmin)
