from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import InegiLocalidad, Zona, Ermita
from .permissions import gerenciaOnly
from .serializers import InegiLocalidadSerializer, ZonaSerializer, \
                         ErmitaSerializer, ErmitaListSerializer


class InegiLocalidadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InegiLocalidad.objects.all()
    serializer_class = InegiLocalidadSerializer


class ZonaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer


class ErmitaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ermita.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ErmitaListSerializer
        return ErmitaSerializer


class ErmitaViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Ermita.objects.all()
    serializer_class = ErmitaListSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
    filename = 'ermitas.xlsx'
