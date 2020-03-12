from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Acopio
from .permissions import gerenciaOrRegion
from .serializers import AcopioSerializer, AcopioTotalsSerializer
from users.permissions import gerenciaOnly


class AcopioViewSet(viewsets.ModelViewSet):
    queryset = Acopio.objects.all().order_by('-fecha')
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            return Acopio.objects.all().order_by('-fecha')
        return Acopio.objects.filter(clave_socio__comunidad__region=self.request.user.clave_socio.comunidad.region).order_by('-fecha')

    def get_serializer_class(self):
        if self.action == 'year_sum':
            return AcopioTotalsSerializer
        return AcopioSerializer

    @action(methods=['get'], detail=False, url_path='year_sum', url_name='year_sum')
    def year_sum(self, request):
        yearly_income = Acopio.objects.values('fecha__year').annotate(year_sum=Sum('ingreso'))
        serializer = self.get_serializer(yearly_income, many=True)
        return Response(serializer.data)


class AcopioViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = AcopioSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOnly]
    filename = 'acopios.xlsx'

    def get_queryset(self):
        queryset = Acopio.objects.all().order_by('-fecha')
        type = self.request.query_params.get('tipo_de_producto', None)
        if type:
            queryset = queryset.filter(tipo_de_producto=type)
        return queryset
