from rest_framework import serializers
from .models import SolicitudCredito


class SolicitudCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudCredito
        fields = '__all__'
