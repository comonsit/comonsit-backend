from datetime import date
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import ContratoCredito
from .permissions import ContratoCreditoPermissions
from .serializers import ContratoCreditoSerializer, ContratoCreditoListSerializer,  \
                         ContratoXLSXSerializer, ContratoUnLinkedSerializer
from .utility import deuda_calculator
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
        elif self.action == 'no_link' or self.action == 'carteras':
            return ContratoUnLinkedSerializer
        return ContratoCreditoSerializer

    # Is Gerencia or Region
    def get_queryset(self):
        q = ContratoCredito.objects.all().order_by('-fecha_inicio')
        if self.action == 'list':
            q = ContratoCredito.objects.filter(estatus=ContratoCredito.DEUDA_PENDIENTE).order_by('-fecha_inicio')
        elif self.action == 'no_link':
            q = q.filter(registrocontable__isnull=True)
        elif self.action == 'carteras':
            cartera_date = self.request.query_params.get('date', date.today())
            q = q.filter(fecha_inicio__lte=cartera_date).filter(
                Q(fecha_final__gt=cartera_date) |
                Q(fecha_final=None)
            )
        if self.request.user.is_gerencia():
            return q
        return q.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region)

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

    @action(methods=['get'], detail=True)
    def deuda(self, request, pk=None):
        credito = self.get_object()
        date_string = request.query_params.get('fecha', None)
        d = date.fromisoformat(date_string) if date_string else date.today()
        deuda = deuda_calculator(credito, d)
        deuda['estatus_detail'] = credito.get_status(d)
        return Response(deuda)

    @action(methods=['get'], detail=False, url_path='no-link', url_name='no-link')
    def no_link(self, request):
        q = self.get_queryset()
        count = q.count()
        serializer = self.get_serializer(q, many=True)
        return Response({'count': count, 'results': serializer.data})

    @action(methods=['get'], detail=False, url_path='carteras', url_name='carteras')
    def carteras(self, request):
        q = self.get_queryset()
        cartera_date = request.query_params.get('date', None)
        detail = request.query_params.get('detail', None)
        d = date.fromisoformat(cartera_date) if cartera_date else date.today()
        vigentes_list = []
        vencidos_list = []
        vigentes_total = 0
        vencidos_total = 0
        for credito in q:
            # Calculate debt or set to zero
            deuda = deuda_calculator(credito, d, True)
            if 'total_deuda' in deuda:
                deuda_cantidad = deuda['total_deuda']
            else:
                deuda_cantidad = 0

            # Assign to corresponding portfolio
            if credito.get_status(d, True) == ContratoCredito.VIGENTE:
                vigentes_list.append(credito)
                vigentes_total += deuda_cantidad
            else:
                vencidos_list.append(credito)
                vencidos_total += deuda_cantidad

        result = {
                'vigentes_total': vigentes_total,
                'vencidos_total': vencidos_total,
                'vigentes_count': len(vigentes_list),
                'vencidos_count': len(vencidos_list)
            }

        if detail:
            serialized_vigentes = self.get_serializer(vigentes_list, many=True)
            serialized_vencidos = self.get_serializer(vencidos_list, many=True)
            result.update({'vigentes': serialized_vigentes.data, 'vencidos': serialized_vencidos.data})
        return Response(result)


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
