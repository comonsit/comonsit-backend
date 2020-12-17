from rest_framework.permissions import BasePermission
from users.models import User


class ContratoCreditoPermissions(BasePermission):
    """
     RU  Gerencia
     R   Region
    """
    def has_permission(self, request, view):
        if request.user.is_gerencia() or request.user.role == User.ROL_PROMOTOR:
            return request.method == "GET" or request.method == "PATCH"
        return False

    def has_object_permission(self, request, view, obj):
        # Is gerencia or Read same Region
        if (request.user.clave_socio.comunidad.region == obj.clave_socio.comunidad.region
                and request.method == "GET"):
            return True
        return request.user.is_gerencia()
