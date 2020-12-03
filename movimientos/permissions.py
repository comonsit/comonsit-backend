from rest_framework.permissions import BasePermission, SAFE_METHODS

CREATE_UPDATE_METHODS = ('POST', 'PUT', 'PATCH')


class gerenciaOrRegion(BasePermission):
    """
    CRU  permission for Gerencia
     R   pemission per Region
    """
    def has_permission(self, request, view):
        if request.method in CREATE_UPDATE_METHODS:
            return request.user.is_gerencia()
        return request.method in SAFE_METHODS

    # TODO: not needed with previous method???
    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia() and not request.method == "DELETE":
            return True
        # TODO: Raise meaningful error attempting to create or read from unauthorized region
        elif request.method in SAFE_METHODS:
            return request.user.clave_socio.comunidad.region == obj.clave_socio.comunidad.region
        return False
