from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import ContratoCredito
from .permissions import ContratoCreditoPermissions
from .serializers import ContratoCreditoSerializer, ContratoCreditoListSerializer, ContratoXLSXSerializer
from pagos.models import Pago
from pagos.serializers import PagoSerializer
from users.permissions import gerenciaOnly


class ContratoCreditoViewSet(viewsets.ModelViewSet):
    queryset = ContratoCredito.objects.all().order_by('-fecha_inicio')
    serializer_class = ContratoCreditoSerializer
    lookup_field = 'pk'  # clave_socio?
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

    @action(methods=['get'], detail=True)
    def pagos(self, request, pk=None):
        credito = self.get_object()
        q = Pago.objects.filter(credito=credito).order_by('-fecha_pago')
        serializer = PagoSerializer(q, many=True)
        return Response(serializer.data)


class ContratoViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ContratoXLSXSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
    filename = 'contratos.xlsx'

    def get_queryset(self):
        all = self.request.query_params.get('all', None)
        if all:
            q = ContratoCredito.objects.all().order_by('-fecha_inicio')
        else:
            q = ContratoCredito.objects.filter(estatus=ContratoCredito.DEUDA_PENDIENTE).order_by('-fecha_inicio')
        region = self.request.query_params.get('region', None)
        if region:
            q = q.filter(clave_socio__comunidad__region=region)
        return q
