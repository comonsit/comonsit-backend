from rest_framework import viewsets

from .models import InegiLocalidad, Zona, Ermita
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
