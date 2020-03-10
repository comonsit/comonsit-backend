from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from .permissions import gerenciaOrRegion

from .models import Socio
from .serializers import SocioSerializer
from users.permissions import gerenciaOrReadOnly


class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer
    lookup_field = 'clave_socio'
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            return Socio.objects.all()

        return Socio.objects.filter(comunidad__region=self.request.user.clave_socio.comunidad.region)


class SocioViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOrReadOnly]
    filename = 'socios.xlsx'
