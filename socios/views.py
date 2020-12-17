from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from .permissions import gerenciaOrRegion

from .models import Socio
from .serializers import SocioSerializer, SocioListSerializer, SocioSerializerXLS
from users.permissions import AllowVisitor


def socios_queryset(self):
    queryset = Socio.objects.all().order_by('clave_socio')
    if not self.request.user.is_gerencia():
        return queryset.filter(comunidad__region=self.request.user.clave_socio.comunidad.region)

    return queryset


class SocioViewSet(viewsets.ModelViewSet):
    lookup_field = 'clave_socio'
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion | AllowVisitor]

    def get_queryset(self):
        return socios_queryset(self)

    def get_serializer_class(self):
        if self.action == 'list':
            return SocioListSerializer
        return SocioSerializer


class SocioViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = SocioSerializerXLS
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]
    filename = 'socios.xlsx'

    def get_queryset(self):
        return socios_queryset(self)
