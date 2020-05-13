from rest_framework.permissions import BasePermission


class gerenciaOrRegion(BasePermission):
    """
    CRU   permission for Gerencia
    CRU   pemission per Region
    """
    def has_permission(self, request, view):
        return request.method == "GET" or request.method == "POST" or request.method == "PATCH"

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        # TODO: Raise meaningful error attempting to create or read from unauthorized region
        return request.user.clave_socio.comunidad.region == obj.credito.clave_socio.comunidad.region
