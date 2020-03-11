from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Acopio
from .permissions import gerenciaOrRegion
from .serializers import AcopioSerializer
from users.permissions import gerenciaOnly


class AcopioViewSet(viewsets.ModelViewSet):
    queryset = Acopio.objects.all().order_by('-fecha')
    serializer_class = AcopioSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            return Acopio.objects.all().order_by('-fecha')
        return Acopio.objects.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha')


class AcopioViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = AcopioSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
    filename = 'acopios.xlsx'

    def get_queryset(self):
        queryset = Acopio.objects.all().order_by('-fecha')
        type = self.request.query_params.get('tipo_de_producto', None)
        if type:
            queryset = queryset.filter(tipo_de_producto=type)
        return queryset
