from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib import admin
from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = ("username", "first_name", "last_name", "role", "is_staff")

    fieldsets = UserAdmin.fieldsets + (
        (None,  {'fields': ('phone', 'role', 'clave_socio')}),
    )


admin.site.register(User, CustomUserAdmin)
