from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROL_SOCIO = 'SO'
    ROL_PROMOTOR = 'PR'
    ROL_COORDINADOR = 'CO'
    ROL_GERENTE = 'GE'
    USER_ROLES = (
        (ROL_SOCIO, 'Socio'),
        (ROL_PROMOTOR, 'Promotor'),
        (ROL_COORDINADOR, 'Coordinador'),
        (ROL_GERENTE, 'Gerente')
    )
    role = models.CharField(max_length=2, choices=USER_ROLES, default=ROL_SOCIO)
    phone = models.CharField(max_length=20, blank=True)
    clave_socio = models.ForeignKey('socios.Socios', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
