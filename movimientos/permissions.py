from rest_framework.permissions import BasePermission
from socios.models import Socio


class gerenciaOrRegion(BasePermission):
    """
    CRU  permission for Gerencia
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
                socio_to_validate = Socio.objects.get(clave_socio=request.data['clave_socio'])
                current_user_socio = request.user.clave_socio
                return socio_to_validate.comunidad.region == current_user_socio.comunidad.region
            return False
        elif request.method == "PUT" or request.method == "PATCH":
            return request.user.is_gerencia()
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_gerencia():
            return True
        # TODO: Raise meaningful error attempting to create or read from unauthorized region
        return request.user.clave_socio.comunidad.region == obj.clave_socio.comunidad.region
