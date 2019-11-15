from rest_framework import viewsets

from .models import Acopios
from .serializers import AcopiosSerializer


class AcopiosViewSet(viewsets.ModelViewSet):
    queryset = Acopios.objects.all()
    serializer_class = AcopiosSerializer
