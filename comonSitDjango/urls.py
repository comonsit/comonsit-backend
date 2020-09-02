"""comonSitDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.gis import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from acopios.views import AcopioViewSet, AcopioViewSetXLSX
from bancos.views import BancoViewSet, SubCuentaViewSet, \
                         MovimientoBancoViewSet, RegistroContableViewSet, \
                         RegistroContableViewSetXLSX
from contratos.views import ContratoCreditoViewSet, ContratoViewSetXLSX
from solicitudes.views import SolicitudCreditoViewSet, ChatSolicitudViewSet
from movimientos.views import MovimientoViewSet, MovimientoConcViewSet
from pagos.views import PagoViewSet, PagoViewSetXLSX
from socios.views import SocioViewSet, SocioViewSetXLSX
from tsumbalil.views import CargoViewSet, CargoCoopViewSet, RegionViewSet, \
                            ComunidadViewSet, EmpresaViewSet, FuenteViewSet, \
                            PuestoViewSet
from users.views import UserViewSet


routers = routers.DefaultRouter()
routers.register(r"acopios", AcopioViewSet)
routers.register(r"acopiosXLSX", AcopioViewSetXLSX, basename='acopiosxlsx')
routers.register(r"cargos", CargoViewSet)
routers.register(r"banco", BancoViewSet, basename='banco')
routers.register(r"contratos", ContratoCreditoViewSet)
routers.register(r"contratosXLSX", ContratoViewSetXLSX, basename='contratosXLSX')
routers.register(r"empresas", EmpresaViewSet)
routers.register(r"fuentes", FuenteViewSet)
routers.register(r"puestos", PuestoViewSet)
routers.register(r"pagos", PagoViewSet, basename='pagos')
routers.register(r"pagosXLSX", PagoViewSetXLSX, basename='pagosXLSX')
routers.register(r"cargos-coop", CargoCoopViewSet, basename='cargos-coop')
routers.register(r"comunidades", ComunidadViewSet)
routers.register(r"movimientos", MovimientoViewSet, basename='movimientos')
routers.register(r"movimientos-conc", MovimientoConcViewSet, basename='movimientos-conc')
routers.register(r"mov-bancos", MovimientoBancoViewSet, basename='mov-bancos')
routers.register(r"solic-creditos", SolicitudCreditoViewSet)
routers.register(r"solic-creditos-comm", ChatSolicitudViewSet, basename='solic-creditos-comm')
routers.register(r"regiones", RegionViewSet)
routers.register(r"registros-contables", RegistroContableViewSet, basename='registros-contables')
routers.register(r"registros-contables-xlsx", RegistroContableViewSetXLSX, basename='registros-contables')
routers.register(r"socios", SocioViewSet)
routers.register(r"sociosXLSX", SocioViewSetXLSX, basename='sociosxlsx')
routers.register(r"subcuentas", SubCuentaViewSet)
routers.register(r"users", UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(routers.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls')),
]
