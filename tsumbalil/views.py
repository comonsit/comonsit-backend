from django.db.models import Q, Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from comonSitDjango.constants import ACTIVO
from .models import Cargo, CargoCoop, Region, Comunidad, Empresa, Puesto_Trabajo, Fuente
from .serializers import CargoSerializer, CargoCoopSerializer, RegionSerializer, \
                         ComunidadSerializer, EmpresaSerializer, PuestoSerializer, \
                         FuenteSerializer, ComunidadSerializerXLSX, ComunidadSociosSerializer
from users.permissions import gerenciaOrReadOnly, ReadOnly


class CargoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class CargoCoopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoCoop.objects.all()
    serializer_class = CargoCoopSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class EmpresaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class ComunidadViewSet(viewsets.ModelViewSet):
    queryset = Comunidad.objects.all()
    permission_classes = [permissions.IsAuthenticated, gerenciaOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'num_socios':
            return ComunidadSociosSerializer
        return ComunidadSerializer

    @action(methods=['get'], detail=False, url_path='num-socios', url_name='num-socios')
    def num_socios(self, request, pk=None):
        q = self.get_queryset()
        q = Comunidad.objects.annotate(
            num_socios_cf=(Count('socio', filter=Q(socio__estatus_cafe=ACTIVO))),
            num_socios_mi=(Count('socio', filter=Q(socio__estatus_miel=ACTIVO))),
            num_socios_ja=(Count('socio', filter=Q(socio__estatus_yip=ACTIVO))),
            num_socios_sl=(Count('socio', filter=Q(socio__estatus_trabajador=ACTIVO)))
            )
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)


class ComunidadViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Comunidad.objects.all()
    serializer_class = ComunidadSerializerXLSX
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOrReadOnly]
    filename = 'comunidades.xlsx'

class PuestoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Puesto_Trabajo.objects.all()
    serializer_class = PuestoSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class FuenteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fuente.objects.all()
    serializer_class = FuenteSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]
