from rest_framework.permissions import BasePermission, SAFE_METHODS


class gerenciaOrRegion(BasePermission):
    """
    CRU permission for Gerencia
     R  pemission per Region
    """
    def has_permission(self, request, view):
        return request.method != "DELETE" and request.user.is_gerencia() or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        return request.user.clave_socio.comunidad.region == obj.comunidad.region
