from rest_framework.permissions import BasePermission
from socios.models import Socio


class gerenciaOrRegion(BasePermission):
    """
    CRUD permission for Gerencia
    CR   pemission per Region
    """
    def has_permission(self, request, view):
        if request.user.is_gerencia() or request.method == "GET":
            return True
        elif request.method == "POST":
            # only create acopios from same region
            # TODO: Verify in Serializer instead??? or verify that clave_socio exists???
            return Socio.objects.get(clave_socio=request.data['clave_socio']).comunidad.region == request.user.clave_socio.comunidad.region
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        # TODO: Raise meaningful error attempting to create or read from unauthorized region
        # only see acopios from same region
        return request.user.clave_socio.comunidad.region == obj.clave_socio.comunidad.region
