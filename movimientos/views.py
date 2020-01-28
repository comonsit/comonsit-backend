from rest_framework import viewsets

from .models import Movimiento
from .serializers import MovimientoSerializer


class MovimientoViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer

    def get_queryset(self):
        queryset = Movimiento.objects.all().order_by('-fecha_entrega')
        clave_socio = self.request.query_params.get('clave_socio', None)
        if clave_socio:
            queryset = queryset.filter(clave_socio=clave_socio)
        # TODO: limit view if no query to ???
        return queryset
