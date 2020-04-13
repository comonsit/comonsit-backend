from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ContratoCredito
from .permissions import ContratoCreditoPermissions
from .serializers import ContratoCreditoSerializer, ContratoCreditoListSerializer


class ContratoCreditoViewSet(viewsets.ModelViewSet):
    queryset = ContratoCredito.objects.all().order_by('-fecha_inicio')
    serializer_class = ContratoCreditoSerializer
    lookup_field = 'folio'  # clave_socio?
    permission_classes = [permissions.IsAuthenticated, ContratoCreditoPermissions]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'all':
            return ContratoCreditoListSerializer
        return ContratoCreditoSerializer

    # Is Gerencia or Owner
    def get_queryset(self):
        if self.action == 'all':
            q = ContratoCredito.objects.all().order_by('-fecha_inicio')
        else:
            q = ContratoCredito.objects.filter(estatus=ContratoCredito.DEUDA_PENDIENTE).order_by('-fecha_inicio')

        if self.request.user.is_gerencia():
            return q
        return q.filter(solicitud__promotor=self.request.user)

    @action(methods=['get'], detail=False)
    def all(self, request):
        q = self.get_queryset()
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)
