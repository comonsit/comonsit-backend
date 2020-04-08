from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound

from .models import SolicitudCredito, ChatSolicitudCredito
from .permissions import SolicitudPermissions, ChatPermissions
from .serializers import SolicitudCreditoSerializer, SolicitudListSerializer, \
    SolicitudPartialUpdateSerializer, ChatSolicitudSerializer


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
        serializer.save(promotor=self.request.user,
                        estatus_solicitud=SolicitudCredito.REVISION,
                        estatus_evaluacion=SolicitudCredito.REVISION
                        )

    # Is Gerencia or Owner
    def get_queryset(self):
        if self.request.user.is_gerencia():
            return SolicitudCredito.objects.all().order_by('-fecha_solicitud')
        return SolicitudCredito.objects.filter(promotor=self.request.user).order_by('-fecha_solicitud')


class ChatSolicitudViewSet(viewsets.ModelViewSet):
    queryset = ChatSolicitudCredito.objects.all().order_by('fecha')
    serializer_class = ChatSolicitudSerializer
    permission_classes = [permissions.IsAuthenticated, ChatPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        solicitud = self.request.query_params.get('solicitud', None)
        if solicitud:
            # TODO: Catch if a non existing solicitud is requested.
            q = ChatSolicitudCredito.objects.filter(solicitud=solicitud).order_by('fecha')
        else:
            raise NotFound()
        owner = SolicitudCredito.objects.get(folio_solicitud=solicitud).promotor
        if self.request.user.is_gerencia() or owner == self.request.user:
            return q
        raise NotFound()