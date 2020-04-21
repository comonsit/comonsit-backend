from rest_framework.permissions import BasePermission


class ContratoCreditoPermissions(BasePermission):
    """
     RU  Gerencia
     R   Owners
    """
    def has_permission(self, request, view):
        return request.method == "GET" or request.method == "PATCH"

    def has_object_permission(self, request, view, obj):
        # Is gerencia or Owner
        if obj.solicitud.promotor == request.user and request.method == "GET":
            return True
        return request.user.is_gerencia()
