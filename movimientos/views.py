from django.db.models import Sum
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movimiento
from .serializers import MovimientoSerializer, MovimientoConcSerializer
from .permissions import gerenciaOrRegion
from users.permissions import gerenciaOnly
from comonSitDjango.constants import PROCESOS_FIELDS, ACTIVO


class MovimientoViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_serializer_class(self):

        if self.request.query_params and 'clave_socio' not in self.request.query_params:
            return MovimientoConcSerializer
        return MovimientoSerializer

    def get_queryset(self):
        if self.request.user.is_gerencia():
            queryset = Movimiento.objects.all().order_by('-fecha_entrega')
        else:
            # TODO: Give REsponse of unAuthorized socio Search.
            queryset = Movimiento.objects.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha_entrega')

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
            # UGLY CODE that filters all movements of selected process
            process_filter = {}
            process_filter[f'clave_socio__{PROCESOS_FIELDS[proceso]}'] = ACTIVO
            queryset = queryset.filter(**process_filter)

        # TODO: limit view if no query to ???
        return queryset

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
