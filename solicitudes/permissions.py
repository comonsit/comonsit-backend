from rest_framework.permissions import BasePermission


class SolicitudPermissions(BasePermission):
    """
    CRU
    """
    def has_permission(self, request, view):
        if request.method == "POST" or request.method == "GET" or request.method == "PATCH":
            return True

    def has_object_permission(self, request, view, obj):
        # Is gerencia or Owner
        return request.user.is_gerencia() or obj.promotor == request.user


class ChatPermissions(BasePermission):
    """
    CR
    """
    def has_permission(self, request, view):
        return request.method == "POST" or request.method == "GET"

    def has_object_permission(self, request, view, obj):
        # Is gerencia or Owner
        return request.user.is_gerencia() or obj.solicitud.promotor == request.user
