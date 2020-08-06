from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import status

from .models import Banco, SubCuenta, MovimientoBanco, RegistroContable
from .serializers import BancoSerializer, SubCuentaSerializer, \
                         MovimientoBancoSerializer, RegistroContableSerializer, \
                         SaldosSerializer
from .permissions import gerenciaOnly


class BancoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banco.objects.all()
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]

    def get_serializer_class(self):
        if self.action == 'saldos':
            return SaldosSerializer
        return BancoSerializer

    @action(methods=['get'], detail=False)
    def saldos(self, request):
        q = self.get_queryset()
        initial_date = request.query_params.get('initialDate', None)
        final_date = request.query_params.get('finalDate', None)
        date_range = Q()
        if initial_date:
            date_range &= Q(subcuenta__registrocontable__movimiento_banco__fecha__gte=initial_date)
        if final_date:
            date_range &= Q(subcuenta__registrocontable__movimiento_banco__fecha__lte=final_date)

        q = q.annotate(
                tot_ingresos=Coalesce(Sum(
                    'subcuenta__registrocontable__cantidad',
                    filter=Q(subcuenta__registrocontable__ingr_egr=True) & date_range), 0),
                tot_egresos=Coalesce(Sum(
                    'subcuenta__registrocontable__cantidad',
                    filter=Q(subcuenta__registrocontable__ingr_egr=False) & date_range), 0)
                )
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)


class SubCuentaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCuenta.objects.filter(sistema=False)
    serializer_class = SubCuentaSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]


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


class RegistroContableViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = RegistroContableSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]

    def get_queryset(self):
        q = RegistroContable.objects.all()

        initial_date = self.request.query_params.get('initialDate', None)
        if initial_date:
            q = q.filter(movimiento_banco__fecha__gte=initial_date)

        final_date = self.request.query_params.get('finalDate', None)
        if final_date:
            q = q.filter(movimiento_banco__fecha__lte=final_date)
        return q.order_by('-movimiento_banco__fecha')
