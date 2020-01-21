from rest_framework import viewsets
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Socio
from .serializers import SocioSerializer


class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer
    lookup_field = 'clave_socio'


class SocioViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer
    renderer_classes = [XLSXRenderer]
    filename = 'socios.xlsx'
