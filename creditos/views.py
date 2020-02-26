from rest_framework import viewsets

from .models import SolicitudCredito
from .serializers import SolicitudCreditoSerializer, SolicitudPartialUpdatelizer


class SolicitudCreditoViewSet(viewsets.ModelViewSet):
    queryset = SolicitudCredito.objects.all().order_by('-fecha_solicitud')
    serializer_class = SolicitudCreditoSerializer
    lookup_field = 'folio_solicitud'

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return SolicitudPartialUpdatelizer
        return SolicitudCreditoSerializer

    def perform_create(self, serializer):
        serializer.save(promotor=self.request.user)
