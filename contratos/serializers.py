from rest_framework import serializers
from .models import ContratoCredito


class ContratoCreditoSerializer(serializers.ModelSerializer):
    promotor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ContratoCredito
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     pass
