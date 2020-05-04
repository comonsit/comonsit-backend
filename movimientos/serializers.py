from datetime import date
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

        aportacion = data.get('aportacion')
        current_user = self.context['request'].user
        if not aportacion and not current_user.is_gerencia():
            raise serializers.ValidationError("Solo gerencia puede registrar Retiros")

        fecha_entrega = data.get('fecha_entrega')
        tipo_de_movimiento = data.get('tipo_de_movimiento')
        today = date.today()
        if (tipo_de_movimiento == Movimiento.EFECTIVO and
                (fecha_entrega.year != today.year or
                 fecha_entrega.month != today.month)):
            raise serializers.ValidationError("Las aportaciones en efectivo sólo pueden ser del mes en curso.")

        return data
