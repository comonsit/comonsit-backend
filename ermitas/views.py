from rest_framework import viewsets

from .models import InegiLocalidad
from .serializers import InegiLocalidadSerializer


class InegiLocalidadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InegiLocalidad.objects.all()
    serializer_class = InegiLocalidadSerializer
