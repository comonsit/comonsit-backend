from rest_framework.permissions import BasePermission


class ContratoCreditoPermissions(BasePermission):
    """
     RU
    """
    def has_permission(self, request, view):
        if request.method == "GET" or request.method == "PUT" or request.method == "PATCH":
            return True

    def has_object_permission(self, request, view, obj):
        # Is gerencia or Owner
        return request.user.is_gerencia() or obj.solicitud.promotor == request.user
