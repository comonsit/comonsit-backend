from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User


class gerenciaOrRegion(BasePermission):
    """
    CRUD permission for Gerencia
     R   pemission per Region
    """
    def has_permission(self, request, view):
        if request.user.is_gerencia():
            return True
        elif request.user.role == User.ROL_PROMOTOR:
            return request.method in SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        # TODO: Raise meaningful error attempting to create or read from unauthorized region
        # only see acopios from same region
        if request.method == "GET" or request.method in SAFE_METHODS:
            return request.user.clave_socio.comunidad.region == obj.clave_socio.comunidad.region
        return False
