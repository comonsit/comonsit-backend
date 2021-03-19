from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User


class gerenciaOrRegion(BasePermission):
    """
    CRU permission for GERENCIA
     R  pemission per Region for PROMOTOR
    """
    def has_permission(self, request, view):
        return (request.user.is_gerencia() and request.method != "DELETE"
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        return request.user.clave_socio.comunidad.region == obj.comunidad.region
