from rest_framework.permissions import BasePermission


class gerenciaOrRegion(BasePermission):
    """
    CRU  permission for Gerencia
    CR   pemission per Region
    """
    def has_permission(self, request, view):
        if request.method == "GET" or request.method == "POST":
            return True
        elif request.method == "PUT" or request.method == "PATCH":
            return request.user.is_gerencia()
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        # TODO: Raise meaningful error attempting to create or read from unauthorized region
        return request.user.clave_socio.comunidad.region == obj.clave_socio.comunidad.region
