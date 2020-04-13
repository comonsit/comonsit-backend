from rest_framework.permissions import BasePermission
from socios.models import Socio


class gerenciaOrRegion(BasePermission):
    """
    CR   permission for Gerencia
    CR   pemission per Region
    """
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        elif request.method == "POST":
            if request.user.is_gerencia():
                return True
            # TODO: Consider moving to create in Serializer
            elif request.data['clave_socio']:
                return Socio.objects.get(clave_socio=request.data['clave_socio']).comunidad.region == request.user.clave_socio.comunidad.region
            return False
        elif request.method == "PUT" or request.method == "PATCH":
            return request.user.is_gerencia()
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        # TODO: Raise meaningful error attempting to create or read from unauthorized region
        return request.user.clave_socio.comunidad.region == obj.clave_socio.comunidad.region