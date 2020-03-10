from rest_framework import viewsets, permissions

from .models import Movimiento
from .serializers import MovimientoSerializer
from .permissions import gerenciaOrRegion


class MovimientoViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            queryset = Movimiento.objects.all().order_by('-fecha_entrega')
        else:
            # TODO: Give REsponse of unAuthorized socio Search.
            queryset = Movimiento.objects.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha_entrega')
        clave_socio = self.request.query_params.get('clave_socio', None)
        if clave_socio:
            queryset = queryset.filter(clave_socio=clave_socio)
        # TODO: limit view if no query to ???
        return queryset
