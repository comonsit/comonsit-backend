from rest_framework import viewsets, permissions

from .models import SolicitudCredito
from .permissions import SolicitudPermissions
from .serializers import SolicitudCreditoSerializer, SolicitudListSerializer, SolicitudPartialUpdateSerializer


class SolicitudCreditoViewSet(viewsets.ModelViewSet):
    queryset = SolicitudCredito.objects.all().order_by('-fecha_solicitud')
    serializer_class = SolicitudCreditoSerializer
    lookup_field = 'folio_solicitud'
    permission_classes = [permissions.IsAuthenticated, SolicitudPermissions]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return SolicitudPartialUpdateSerializer
        if self.action == 'list':
            return SolicitudListSerializer
        return SolicitudCreditoSerializer

    def perform_create(self, serializer):
        serializer.save(promotor=self.request.user)

    # Is Gerencia or Owner
    def get_queryset(self):
        if self.request.user.is_gerencia():
            return SolicitudCredito.objects.all().order_by('-fecha_solicitud')
        return SolicitudCredito.objects.filter(promotor=self.request.user).order_by('-fecha_solicitud')
