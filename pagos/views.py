from rest_framework import viewsets, permissions

from .models import Pago
from .serializers import PagoSerializer
from .permissions import gerenciaOrRegion


class PagoViewSet(viewsets.ModelViewSet):
    serializer_class = PagoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            queryset = Pago.objects.all().order_by('-fecha_pago')
        else:
            # TODO: Give Response of unAuthorized socio Search.
            queryset = Pago.objects.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha_pago')
        clave_socio = self.request.query_params.get('clave_socio', None)
        if clave_socio:
            queryset = queryset.filter(clave_socio=clave_socio)
        # TODO: limit view if no query to ???
        return queryset
