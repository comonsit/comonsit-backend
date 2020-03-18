from django.db.models import Sum
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movimiento
from .serializers import MovimientoSerializer
from .permissions import gerenciaOrRegion


class MovimientoViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            queryset = Movimiento.objects.all().order_by('-fecha_entrega')
        else:
            # TODO: Give REsponse of unAuthorized socio Search.
            queryset = Movimiento.objects.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha_entrega')
        clave_socio = self.request.query_params.get('clave_socio', None)
        if clave_socio:
            queryset = queryset.filter(clave_socio=clave_socio)
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
