from rest_framework import serializers
from .models import Movimiento


class MovimientoSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Movimiento
        fields = "__all__"

    def validate(self, data):
        """
        Check that user is active in requested process
        """
        # TODO: Move to a general access
        procesos = {
            'CF': 'estatus_cafe',
            'MI': 'estatus_miel',
            'JA': 'estatus_yip',
            'SL': 'estatus_trabajador'
        }
        process_status = getattr(data['clave_socio'], procesos[data['proceso']])
        if process_status != 'AC':
            raise serializers.ValidationError("El Socio no está activo en este proceso")
        return data
