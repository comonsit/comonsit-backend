from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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
        elif self.action == 'list' or self.action == 'no_link':
            return PagoListSerializer
        return PagoSerializer

    def get_queryset(self):
        queryset = Pago.objects.all().order_by('-fecha_pago')
        if not self.request.user.is_gerencia():
            queryset = queryset.filter(credito__clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region)
        elif self.action == 'no_link':
            queryset = queryset.filter(registrocontable__isnull=True)

        # TODO: Give Response of unAuthorized socio Search.
        clave_socio = self.request.query_params.get('clave_socio', None)
        if clave_socio:
            queryset = queryset.filter(clave_socio=clave_socio)
        # TODO: limit view if no query to ???
        return queryset

    @action(methods=['get'], detail=False, url_path='no-link', url_name='no-link')
    def no_link(self, request):
        q = self.get_queryset()
        count = q.count()
        serializer = self.get_serializer(q, many=True)
        return Response({'count': count, 'results': serializer.data})


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
