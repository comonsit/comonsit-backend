from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import Banco, SubCuenta, MovimientoBanco, RegistroContable
from .serializers import BancoSerializer, SubCuentaSerializer, \
                         MovimientoBancoSerializer, RegistroContableSerializer
from .permissions import gerenciaOnly


class BancoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]


class SubCuentaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCuenta.objects.all()
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
    queryset = RegistroContable.objects.all().order_by('-movimiento_banco__fecha')
    serializer_class = RegistroContableSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
