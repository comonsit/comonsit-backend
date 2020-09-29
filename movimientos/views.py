from django.db.models import Sum
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Movimiento
from .serializers import MovimientoSerializer, MovimientoConcSerializer, \
                         MovimientoPartialUpdateSerializer, MovimientoSingleSerializer
from .permissions import gerenciaOrRegion
from users.permissions import gerenciaOnly


def movimientos_queryset(self):
    if self.request.user.is_gerencia():
        queryset = Movimiento.objects.all().order_by('-fecha_entrega')
    else:
        # TODO: Give REsponse of unAuthorized socio Search.
        queryset = Movimiento.objects.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha_entrega')

    # TODO: More automatic process??
    clave_socio = self.request.query_params.get('clave_socio', None)
    if clave_socio:
        queryset = queryset.filter(clave_socio=clave_socio)

    region = self.request.query_params.get('region', None)
    if region:
        queryset = queryset.filter(clave_socio__comunidad__region=region)

    comunidad = self.request.query_params.get('comunidad', None)
    if comunidad:
        queryset = queryset.filter(clave_socio__comunidad=comunidad)

    fuente = self.request.query_params.get('fuente', None)
    if fuente:
        queryset = queryset.filter(clave_socio__fuente=fuente)

    empresa = self.request.query_params.get('empresa', None)
    if empresa:
        queryset = queryset.filter(clave_socio__empresa=empresa)

    proceso = self.request.query_params.get('proceso', None)
    if proceso:
        queryset = queryset.filter(proceso=proceso)
    # TODO: limit view if no query to ???
    return queryset


class MovimientoViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_serializer_class(self):

        if self.action == 'partial_update':
            return MovimientoPartialUpdateSerializer
        elif self.action == 'retrieve':
            return MovimientoSingleSerializer
        elif self.action == 'create':
            return MovimientoSerializer
        return MovimientoConcSerializer

    def get_queryset(self):
        return movimientos_queryset(self)

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

    @action(methods=['get'], detail=False, url_path='saldo', url_name='saldo')
    def saldo(self, request, lookup=None):
        clave_socio = request.query_params.get('clave_socio', None)
        if clave_socio:
            q = self.get_queryset()
            if q.count() == 0:
                return Response({'message': 'No hay información disponible'})
            a = q.filter(aportacion=True).aggregate(total=Sum('monto'))['total']
            r = q.filter(aportacion=False).aggregate(total=Sum('monto'))['total']
            aportaciones = a if a else 0
            retiros = r if r else 0
            total = aportaciones - retiros
            return Response({'saldo': total, 'aportaciones': aportaciones, 'retiros': retiros})
        return Response({'message': 'Agrega la clave de un socio a consultar'})


class MovimientoConcViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movimiento.objects.filter(registrocontable__isnull=True).order_by('-fecha_entrega')
    serializer_class = MovimientoConcSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]

    def list(self, request):
        q = self.get_queryset()
        count = q.count()
        serializer = self.get_serializer(q, many=True)
        return Response({'count': count, 'results': serializer.data})


class MovimientoViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = MovimientoConcSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
    filename = 'aportaciones_retiros.xlsx'

    def get_queryset(self):
        return movimientos_queryset(self)
