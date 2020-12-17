from django.db.models import Sum, Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Acopio
from .permissions import gerenciaOrRegion
from .serializers import AcopioSerializer, AcopioTotalsSerializer
from users.permissions import AllowVisitor


class AcopioViewSet(viewsets.ModelViewSet):
    queryset = Acopio.objects.all().order_by('-fecha')
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion | AllowVisitor]

    def get_queryset(self):
        if self.request.user.is_gerencia():
            return Acopio.objects.all().order_by('-fecha')
        user_region = self.request.user.clave_socio.comunidad.region
        return Acopio.objects.filter(clave_socio__comunidad__region=user_region).order_by('-fecha')

    def get_serializer_class(self):
        if self.action == 'year_sum':
            return AcopioTotalsSerializer
        return AcopioSerializer

    @action(methods=['get'], detail=False, url_path='year_sum', url_name='year_sum')
    def year_sum(self, request):
        query = Acopio.objects.all().order_by('fecha__year')
        clave_socio = request.query_params.get('clave_socio', None)
        comunidad = request.query_params.get('comunidad', None)
        region = request.query_params.get('region', None)
        # TODO: Validate if correct queries
        if clave_socio:
            query = query.filter(clave_socio=clave_socio)
        elif comunidad:
            query = query.filter(clave_socio__comunidad=comunidad)
        elif region:
            query = query.filter(clave_socio__comunidad__region=region)

        q = query.values('fecha__year').annotate(
                year_sum_cf=Sum('ingreso', filter=Q(tipo_de_producto='CF')),
                year_sum_mi=Sum('ingreso', filter=Q(tipo_de_producto='MI')),
                year_sum_ja=Sum('ingreso', filter=Q(tipo_de_producto='JA')),
                year_sum_sl=Sum('ingreso', filter=Q(tipo_de_producto='SL'))
                )
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)


class AcopioViewSetXLSX(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = AcopioSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [permissions.IsAuthenticated, gerenciaOrRegion]
    filename = 'acopios.xlsx'

    def get_queryset(self):
        queryset = Acopio.objects.all().order_by('-fecha')
        if not self.request.user.is_gerencia():
            user_region = self.request.user.clave_socio.comunidad.region
            queryset = Acopio.objects.filter(clave_socio__comunidad__region=user_region).order_by('-fecha')
        type = self.request.query_params.get('tipo_de_producto', None)
        if type:
            queryset = queryset.filter(tipo_de_producto=type)
        return queryset
