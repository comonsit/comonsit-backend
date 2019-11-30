from rest_framework import serializers
from .models import SolicitudCredito


class SolicitudCreditoSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SolicitudCredito
        fields = '__all__'
