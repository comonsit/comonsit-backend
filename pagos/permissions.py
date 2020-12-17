from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User
from users.permissions import CREATE_UPDATE_METHODS


class gerenciaOrRegion(BasePermission):
    """
    CRU   permission for GERENCIA
    CRU   pemission per Region PROMOTOR
    """
    def has_permission(self, request, view):
        if request.user.is_gerencia() or request.user.role == User.ROL_PROMOTOR:
            return request.method in CREATE_UPDATE_METHODS or request.method in SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        # TODO: Raise meaningful error attempting to create or read from unauthorized region
        return request.user.clave_socio.comunidad.region == obj.credito.clave_socio.comunidad.region
