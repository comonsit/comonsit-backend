from rest_framework import viewsets

from .models import Cargos, Regiones, Comunidades
from .serializers import CargosSerializer, RegionesSerializer, ComunidadesSerializer


class CargosViewSet(viewsets.ModelViewSet):
    queryset = Cargos.objects.all()
    serializer_class = CargosSerializer



class RegionesViewSet(viewsets.ModelViewSet):
    queryset = Regiones.objects.all()
    serializer_class = RegionesSerializer



class ComunidadesViewSet(viewsets.ModelViewSet):
    queryset = Comunidades.objects.all()
    serializer_class = ComunidadesSerializer
