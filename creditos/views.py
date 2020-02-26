from rest_framework import viewsets

from .models import SolicitudCredito
from .serializers import SolicitudCreditoSerializer, SolicitudListSerializer, SolicitudPartialUpdateSerializer


class SolicitudCreditoViewSet(viewsets.ModelViewSet):
    queryset = SolicitudCredito.objects.all().order_by('-fecha_solicitud')
    serializer_class = SolicitudCreditoSerializer
    lookup_field = 'folio_solicitud'

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return SolicitudPartialUpdateSerializer
        if self.action == 'list':
            return SolicitudListSerializer
        return SolicitudCreditoSerializer

    def perform_create(self, serializer):
        serializer.save(promotor=self.request.user)
