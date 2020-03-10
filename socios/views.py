from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Socio
from .serializers import SocioSerializer
from users.permissions import gerenciaOnly


class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer
    lookup_field = 'clave_socio'

    def get_queryset(self):
        if self.request.user.is_gerencia():
            return Socio.objects.all()

        return Socio.objects.filter(comunidad__region=self.request.user.clave_socio.comunidad.region)


class SocioViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
    filename = 'socios.xlsx'
