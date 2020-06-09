from rest_framework import viewsets, permissions

from .models import Banco, SubCuenta, MovimientoBanco, RegistroContable
from .serializers import BancoSerializer, SubCuentaSerializer, \
                         MovimientoBancoSerializer, RegistroContableSerializer
from .permissions import gerenciaOnly
from users.permissions import ReadOnly


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


class RegistroContableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegistroContable.objects.all()
    serializer_class = RegistroContableSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
