from rest_framework import viewsets

from .models import InegiLocalidad, Zona
from .serializers import InegiLocalidadSerializer, ZonaSerializer


class InegiLocalidadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InegiLocalidad.objects.all()
    serializer_class = InegiLocalidadSerializer


class ZonaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
