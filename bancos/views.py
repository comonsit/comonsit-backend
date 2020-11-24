from django.db.models import Sum, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import status
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Banco, SubCuenta, MovimientoBanco, RegistroContable
from .serializers import BancoSerializer, SubCuentaSerializer, \
                         MovimientoBancoSerializer, RegistroContableSerializer, \
                         SaldosBancoSerializer, RegistroXLSXSerializer, \
                         SaldosSubcuentaSerializer
from .permissions import gerenciaOnly


class BancoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banco.objects.all()
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]

    def get_serializer_class(self):
        if self.action == 'saldos':
            return SaldosBancoSerializer
        return BancoSerializer

    @action(methods=['get'], detail=False)
    def saldos(self, request):
        q = self.get_queryset()
        initial_date = request.query_params.get('initialDate', None)
        final_date = request.query_params.get('finalDate', None)
        date_range = Q()
        prev_date = Q(False)
        if initial_date:
            date_range &= Q(subcuenta__registrocontable__movimiento_banco__fecha__gte=initial_date)
            prev_date = Q(subcuenta__registrocontable__movimiento_banco__fecha__lt=initial_date)
            q = q.annotate(tot_ingresos_prev=Coalesce(Sum('subcuenta__registrocontable__cantidad',
                                                          filter=Q(subcuenta__registrocontable__ingr_egr=True) & prev_date),
                                                      0),
                           tot_egresos_prev=Coalesce(Sum('subcuenta__registrocontable__cantidad',
                                                         filter=Q(subcuenta__registrocontable__ingr_egr=False) & prev_date),
                                                     0))
        else:
            q = q.annotate(tot_ingresos_prev=Value(0, DecimalField()),
                           tot_egresos_prev=Value(0, DecimalField()),)

        if final_date:
            date_range &= Q(subcuenta__registrocontable__movimiento_banco__fecha__lte=final_date)

        q = q.annotate(tot_ingresos=Coalesce(Sum('subcuenta__registrocontable__cantidad',
                                                 filter=Q(subcuenta__registrocontable__ingr_egr=True) & date_range),
                                             0),
                       tot_egresos=Coalesce(Sum('subcuenta__registrocontable__cantidad',
                                                filter=Q(subcuenta__registrocontable__ingr_egr=False) & date_range),
                                            0))
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)


class SubCuentaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCuenta.objects.filter(sistema=False)
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]

    def get_serializer_class(self):
        if self.action == 'saldos':
            return SaldosSubcuentaSerializer
        return SubCuentaSerializer

    def get_queryset(self):
        q = SubCuenta.objects.all().order_by('id_contable')
        if self.action == 'list':
            return q.filter(sistema=False)
        return q

    # TODO: code duplicated with Bancos Saldos Action & serializer
    @action(methods=['get'], detail=False)
    def saldos(self, request):
        q = self.get_queryset()
        initial_date = request.query_params.get('initialDate', None)
        final_date = request.query_params.get('finalDate', None)
        date_range = Q()
        prev_date = Q(False)
        if initial_date:
            date_range &= Q(registrocontable__movimiento_banco__fecha__gte=initial_date)
            prev_date = Q(registrocontable__movimiento_banco__fecha__lt=initial_date)
            q = q.annotate(tot_ingresos_prev=Coalesce(Sum('registrocontable__cantidad',
                                                          filter=Q(registrocontable__ingr_egr=True) & prev_date),
                                                      0),
                           tot_egresos_prev=Coalesce(Sum('registrocontable__cantidad',
                                                         filter=Q(registrocontable__ingr_egr=False) & prev_date),
                                                     0))
        else:
            q = q.annotate(
                tot_ingresos_prev=Value(0, DecimalField()),
                tot_egresos_prev=Value(0, DecimalField()),
            )

        if final_date:
            date_range &= Q(registrocontable__movimiento_banco__fecha__lte=final_date)

        q = q.annotate(
                tot_ingresos=Coalesce(Sum(
                    'registrocontable__cantidad',
                    filter=Q(registrocontable__ingr_egr=True) & date_range), 0),
                tot_egresos=Coalesce(Sum(
                    'registrocontable__cantidad',
                    filter=Q(registrocontable__ingr_egr=False) & date_range), 0)
                )
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)


class MovimientoBancoViewSet(viewsets.ModelViewSet):
    queryset = MovimientoBanco.objects.all()
    serializer_class = MovimientoBancoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = {
            "registros_nvos": str(RegistroContable.objects.filter(movimiento_banco=serializer.instance).count()),
            "movimientoBanco": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


def registros_queryset(self):
    q = RegistroContable.objects.all()

    initial_date = self.request.query_params.get('initialDate', None)
    if initial_date:
        q = q.filter(movimiento_banco__fecha__gte=initial_date)

    final_date = self.request.query_params.get('finalDate', None)
    if final_date:
        q = q.filter(movimiento_banco__fecha__lte=final_date)
    return q.order_by('-movimiento_banco__fecha')


class RegistroContableViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]

    def get_queryset(self):
        return registros_queryset(self)

    def get_serializer_class(self):
        if self.action == 'list':
            return RegistroContableSerializer
        return RegistroXLSXSerializer


class RegistroContableViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = RegistroXLSXSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
    filename = 'registrosBanco.xlsx'

    def get_queryset(self):
        return registros_queryset(self)
