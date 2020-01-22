from rest_framework import permissions


class IsGerencia(permissions.BasePermission):
    """
    CRUD permission for Gerencia
     R  pemission for all
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_gerencia()
