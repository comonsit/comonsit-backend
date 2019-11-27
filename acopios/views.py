from rest_framework import viewsets

from .models import Acopio
from .serializers import AcopioSerializer


class AcopioViewSet(viewsets.ModelViewSet):
    queryset = Acopio.objects.all()
    serializer_class = AcopioSerializer
