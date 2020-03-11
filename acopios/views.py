from rest_framework import viewsets, permissions

from .models import Acopio
from .permissions import gerenciaOrRegion
from .serializers import AcopioSerializer


class AcopioViewSet(viewsets.ModelViewSet):
    queryset = Acopio.objects.all().order_by('-fecha')
    serializer_class = AcopioSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            return Acopio.objects.all().order_by('-fecha')
        return Acopio.objects.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha')
