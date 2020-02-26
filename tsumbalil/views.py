from rest_framework import viewsets, permissions

from .models import Cargo, CargoCoop, Region, Comunidad, Empresa
from .serializers import CargoSerializer, CargoCoopSerializer, RegionSerializer, ComunidadSerializer, EmpresaSerializer
from .permissions import IsGerencia


class CargoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class CargoCoopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoCoop.objects.all()
    serializer_class = CargoCoopSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class EmpresaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class ComunidadViewSet(viewsets.ModelViewSet):
    queryset = Comunidad.objects.all()
    serializer_class = ComunidadSerializer
    # permission_classes = [permissions.IsAuthenticated, IsGerencia]
