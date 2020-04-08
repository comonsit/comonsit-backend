from rest_framework import viewsets, permissions

from .models import ContratoCredito
from .permissions import ContratoCreditoPermissions
from .serializers import ContratoCreditoSerializer, ContratoCreditoListSerializer


class ContratoCreditoViewSet(viewsets.ModelViewSet):
    queryset = ContratoCredito.objects.all().order_by('-fecha_inicio')
    serializer_class = ContratoCreditoSerializer
    lookup_field = 'folio'  # clave_socio?
    permission_classes = [permissions.IsAuthenticated, ContratoCreditoPermissions]

    def get_serializer_class(self):
        if self.action == 'list':
            return ContratoCreditoListSerializer
        return ContratoCreditoSerializer

    # Is Gerencia or Owner
    def get_queryset(self):
        if self.request.user.is_gerencia():
            return ContratoCredito.objects.all().order_by('-fecha_inicio')
        return ContratoCredito.objects.filter(promotor=self.request.user).order_by('-fecha_inicio')
