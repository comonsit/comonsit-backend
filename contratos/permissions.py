from rest_framework.permissions import BasePermission


class ContratoCreditoPermissions(BasePermission):
    """
     RU  Gerencia
     R   Region
    """
    def has_permission(self, request, view):
        return request.method == "GET" or request.method == "PATCH"

    def has_object_permission(self, request, view, obj):
        # Is gerencia or Read same Region
        if (request.user.clave_socio.comunidad.region == obj.clave_socio.comunidad.region
                and request.method == "GET"):
            return True
        return request.user.is_gerencia()
