from rest_framework.permissions import BasePermission


class gerenciaOnly(BasePermission):
    """
    CRU  permission for Gerencia except delete
         No pemissions for others
    """
    def has_permission(self, request, view):
        return request.method != "DELETE" and request.user.is_gerencia()
