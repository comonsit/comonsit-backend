from rest_framework import serializers
from .models import SolicitudCredito, ChatSolicitudCredito
from contratos.models import ContratoCredito
from contratos.serializers import ContratoCreditoSerializer
from users.models import User


class ChatSolStartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChatSolicitudCredito
        fields = '__all__'
        read_only_fields = ('solicitud', 'user')


class SolicitudCreditoSerializer(serializers.ModelSerializer):
    promotor = serializers.StringRelatedField(read_only=True)
    estatus_solicitud = serializers.CharField(read_only=True)
    estatus_evaluacion = serializers.CharField(read_only=True)
    nombre_productor = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    comunidad = serializers.SerializerMethodField(read_only=True)
    # area = serializers.SerializerMethodField(read_only=True)
    aval_nombre = serializers.SerializerMethodField(read_only=True)
    cargo = serializers.SerializerMethodField(read_only=True)
    cargo_coop = serializers.SerializerMethodField(read_only=True)
    # cargo_mision = serializers.SerializerMethodField(read_only=True)
    fecha_ingr_yomol_atel = serializers.SerializerMethodField(read_only=True)
    chat = ChatSolStartSerializer(many=True)
    tipo_credito_nombre = serializers.SerializerMethodField(read_only=True)
    act_productiva_nombre = serializers.SerializerMethodField(read_only=True)
    mot_credito_nombre = serializers.SerializerMethodField(read_only=True)
    proceso_nombre = serializers.SerializerMethodField(read_only=True)
    contrato = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SolicitudCredito
        fields = '__all__'

    def get_nombre_productor(self, object):
        return object.clave_socio.nombres + ' ' + object.clave_socio.apellido_paterno \
                + ' ' + object.clave_socio.apellido_materno

    def get_region(self, object):
        return object.clave_socio.comunidad.region.id

    def get_comunidad(self, object):
        return object.clave_socio.comunidad.nombre_de_comunidad

    def get_aval_nombre(self, object):
        return object.aval.nombres + ' ' + object.aval.apellido_paterno + ' ' + object.aval.apellido_materno

    def get_cargo(self, object):
        return object.clave_socio.cargo.nombre_de_cargo

    def get_cargo_coop(self, object):
        return ', '.join([c.nombre_cargo_coop for c in object.clave_socio.cargo_coop.all()])

    def get_fecha_ingr_yomol_atel(self, object):
        return object.clave_socio.fecha_ingr_yomol_atel

    def get_tipo_credito_nombre(self, object):
        return object.get_tipo_credito_display()

    def get_act_productiva_nombre(self, object):
        return object.get_act_productiva_display()

    def get_mot_credito_nombre(self, object):
        return object.get_mot_credito_display()

    def get_proceso_nombre(self, object):
        return object.get_proceso_display()

    def get_contrato(self, object):
        if ContratoCredito.objects.filter(solicitud=object).exists():
            return object.contrato.folio
        return None

    def validate(self, data):
        """
        Check that requestor and authorizor are not the same
        """
        if data['clave_socio'] == data['aval']:
            raise serializers.ValidationError("Aval y Solicitante deben ser diferentes")
        """
        Check for recent duplicates
        """
        if SolicitudCredito.objects.filter(
           clave_socio=data['clave_socio']).filter(
           fecha_solicitud=data['fecha_solicitud']).filter(
           monto_solicitado=data['monto_solicitado']):
            raise serializers.ValidationError("Ya existe un crédito con esa fecha y monto")

        return data

    def create(self, validated_data):
        comentario_data = validated_data.pop('chat')
        instance = SolicitudCredito.objects.create(**validated_data)
        # Only one comment will be saved upon create
        ChatSolicitudCredito.objects.create(solicitud=instance, user=self.context['request'].user, **comentario_data[0])
        return instance


class SolicitudListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudCredito
        fields = ['folio_solicitud', 'fecha_solicitud', 'clave_socio', 'tipo_credito', 'monto_solicitado',
                  'plazo_de_pago_solicitado', 'estatus_solicitud', 'estatus_evaluacion']


class SolicitudPartialUpdateSerializer(serializers.ModelSerializer):
    promotor = serializers.StringRelatedField(read_only=True)
    chat = ChatSolStartSerializer(many=True)
    contrato = ContratoCreditoSerializer()
    monto_aprobado = serializers.DecimalField(max_digits=9, decimal_places=2, write_only=True)
    plazo_aprobado = serializers.IntegerField(min_value=1, write_only=True)
    contrato = serializers.SerializerMethodField(read_only=True)

    def get_contrato(self, object):
        if ContratoCredito.objects.filter(solicitud=object).exists():
            return object.contrato.folio
        return None

    class Meta:
        model = SolicitudCredito
        fields = '__all__'

    def update(self, instance, validated_data):
        current_user = self.context['request'].user
        comentario_data = validated_data.pop('chat')
        solicitud_status = validated_data.get('estatus_solicitud', None)
        eval_status = validated_data.get('estatus_evaluacion', None)

        if solicitud_status:
            if current_user.role == User.ROL_PROMOTOR:
                # Promotor requesting revision
                if solicitud_status and solicitud_status != SolicitudCredito.APROBADO:
                    instance.estatus_solicitud = solicitud_status
                else:
                    raise serializers.ValidationError("Promotores sólo pueden solicitar revisiones")
            elif current_user.is_gerencia():
                instance.estatus_solicitud = solicitud_status
                instance.irregularidades = validated_data.get('irregularidades', instance.irregularidades)
                instance.pregunta_1 = validated_data.get('pregunta_1', instance.pregunta_1)
                instance.pregunta_2 = validated_data.get('pregunta_2', instance.pregunta_2)
                instance.pregunta_3 = validated_data.get('pregunta_3', instance.pregunta_3)
                instance.pregunta_4 = validated_data.get('pregunta_4', instance.pregunta_4)
        elif eval_status:
            if current_user.role == User.ROL_GERENTE:
                instance.estatus_evaluacion = validated_data.get('estatus_evaluacion', instance.estatus_evaluacion)
                monto_aprobado = validated_data.get('monto_aprobado', None)
                plazo_aprobado = validated_data.get('plazo_aprobado', None)

                # Approve and Create new Credit Contract
                if instance.estatus_evaluacion == SolicitudCredito.APROBADO and monto_aprobado and plazo_aprobado:
                    ContratoCredito.objects.create(
                        solicitud=instance,
                        clave_socio=instance.clave_socio,
                        promotor=instance.promotor, monto=monto_aprobado,
                        plazo=plazo_aprobado,
                        estatus=ContratoCredito.EN_CURSO,
                        estatus_efectivo=ContratoCredito.POR_COBRAR,
                        estatus_ejecucion=ContratoCredito.POR_COBRAR
                    )

            # Promotor/Coord requesting reNegotiation
            elif(eval_status == SolicitudCredito.REVISION and
                    instance.estatus_evaluacion == SolicitudCredito.NEGOCIACION and
                    instance.estatus_solicitud == SolicitudCredito.APROBADO):
                print('ACTUALIZANDO el estatus eval...')
                instance.estatus_evaluacion = eval_status
        else:
            raise serializers.ValidationError("Patch inesperado")

        ChatSolicitudCredito.objects.create(solicitud=instance, user=current_user, **comentario_data[0])
        instance.save()
        return instance


class ChatSolicitudSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChatSolicitudCredito
        fields = '__all__'

    def create(self, validated_data):
        current_user = self.context['request'].user
        solicitud = validated_data.pop('solicitud', None)

        # Only Gerencia or Creators of Solicitud can comment.
        if solicitud.promotor != current_user and not current_user.is_gerencia():
            raise serializers.ValidationError({
                'message': 'No tienes permiso para comentar en esta Solicitud'
            })

        chat = ChatSolicitudCredito.objects.create(solicitud=solicitud, **validated_data)
        return chat
