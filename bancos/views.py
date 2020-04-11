from rest_framework import viewsets, permissions

from .models import ConceptoBanco, SubCuenta, MovimientoBanco
from .serializers import ConceptoBancoSerializer, SubCuentaSerializer, \
                         MovimientoBancoSerializer
from .permissions import gerenciaOnly
from users.permissions import ReadOnly


class ConceptoBancoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConceptoBanco.objects.all()
    serializer_class = ConceptoBancoSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class SubCuentaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCuenta.objects.all()
    serializer_class = SubCuentaSerializer
    permission_classes = [permissions.IsAuthenticated, ReadOnly]


class MovimientoBancoViewSet(viewsets.ModelViewSet):
    queryset = MovimientoBanco.objects.all()
    serializer_class = MovimientoBancoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
