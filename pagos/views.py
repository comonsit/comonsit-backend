from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Pago
from .serializers import PagoSerializer, PagoListSerializer, PagoPartialUpdateSerializer
from .permissions import gerenciaOrRegion


class PagoViewSet(viewsets.ModelViewSet):
    serializer_class = PagoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return PagoPartialUpdateSerializer
        elif self.action == 'list':
            return PagoListSerializer
        return PagoSerializer

    def get_queryset(self):
        if self.request.user.is_gerencia():
            queryset = Pago.objects.all().order_by('-fecha_pago')
        else:
            queryset = Pago.objects.filter(credito__clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha_pago')
        # TODO: Give Response of unAuthorized socio Search.
        clave_socio = self.request.query_params.get('clave_socio', None)
        if clave_socio:
            queryset = queryset.filter(clave_socio=clave_socio)
        # TODO: limit view if no query to ???
        return queryset


class PagoViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PagoSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]
    filename = 'pagos.xlsx'

    def get_queryset(self):
        if self.request.user.is_gerencia():
            queryset = Pago.objects.all().order_by('-fecha_pago')
        else:
            queryset = Pago.objects.filter(credito__clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha_pago')
        # TODO: Pagination limit?
        return queryset
