from rest_framework import serializers
from .models import SolicitudCredito


class SolicitudCreditoSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SolicitudCredito
        fields = '__all__'

    def validate(self, data):
        """
        Check that requestor and authorizor are not the same
        """
        if data['clave_socio'] == data['aval']:
            raise serializers.ValidationError("Aval y Solicitante deben ser diferentes")
        return data
