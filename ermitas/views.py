from rest_framework import viewsets

from .models import InegiLocalidad, Zona, Ermita
from .serializers import InegiLocalidadSerializer, ZonaSerializer, \
                         ErmitaSerializer


class InegiLocalidadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InegiLocalidad.objects.all()
    serializer_class = InegiLocalidadSerializer


class ZonaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer


class ErmitaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ermita.objects.all()
    serializer_class = ErmitaSerializer
