from rest_framework import viewsets

from .models import Cargo, CargoCoop, Region, Comunidad
from .serializers import CargoSerializer, CargoCoopSerializer, RegionSerializer, ComunidadSerializer


class CargoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class CargoCoopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoCoop.objects.all()
    serializer_class = CargoCoopSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class ComunidadViewSet(viewsets.ModelViewSet):
    queryset = Comunidad.objects.all()
    serializer_class = ComunidadSerializer
