from rest_framework import viewsets, permissions

from .models import Cargo, CargoCoop, Region, Comunidad, Empresa, Puesto_Trabajo, Fuente
from .serializers import CargoSerializer, CargoCoopSerializer, RegionSerializer, \
                         ComunidadSerializer, EmpresaSerializer, PuestoSerializer, \
                         FuenteSerializer, SubCuentaSerializer
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
    serializer_class = ComunidadSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrReadOnly]


class PuestoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Puesto_Trabajo.objects.all()
    serializer_class = PuestoSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class FuenteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fuente.objects.all()
    serializer_class = FuenteSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class SubCuentaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fuente.objects.all()
    serializer_class = SubCuentaSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]
