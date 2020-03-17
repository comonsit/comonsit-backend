from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from .permissions import gerenciaOrRegion

from .models import Socio
from .serializers import SocioSerializer, SocioListSerializer, SocioSerializerXLS
from users.permissions import gerenciaOnly


class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all()
    lookup_field = 'clave_socio'
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            return Socio.objects.all()

        return Socio.objects.filter(comunidad__region=self.request.user.clave_socio.comunidad.region)

    def get_serializer_class(self):
        if self.action == 'list':
            return SocioListSerializer
        return SocioSerializer


class SocioViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializerXLS
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
    filename = 'socios.xlsx'
