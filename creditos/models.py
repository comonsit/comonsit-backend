from django.db import models


class SolicitudCredito(models.Model):

    MICROCREDITO = 'MC'
    CREDITO_PRODUCTIVO = 'CP'
    TIPO_CREDITO_CHOICES = [
        (MICROCREDITO, 'Microcrédito'),
        (CREDITO_PRODUCTIVO, 'Crédito Productivo')
    ]

    CAFETAL = 'CA'
    VIVEROS = 'VI'
    HORTALIZAS = 'HR'
    GAN_VACUNO_ENG = 'GE'
    GAN_VACUNO_CRIA = 'GC'
    GAN_PORCINO_ENG = 'PE'
    GAN_PORCINO_CRIA = 'PC'
    AVE_TRASPATIO = 'AT'
    MILPA = 'MI'
    ELAB_ALIMENTOS = 'EL'
    ELAB_ARTESANIA = 'ER'
    HERRAMIENTA = 'HE'
    OTRO = 'OT'
    TIPO_ACTIV_PROD_CHOICES = [
        (CAFETAL, 'Cafetal'),
        (VIVEROS, 'Viveros'),
        (HORTALIZAS, 'Hortalizas'),
        (GAN_VACUNO_ENG, 'Ganado Vacuno (engorda)'),
        (GAN_VACUNO_CRIA, 'Ganado Vacuno (pie de cría)'),
        (GAN_PORCINO_ENG, 'Ganado Porcino (engorda)'),
        (GAN_PORCINO_CRIA, 'Ganado Porcino (pie de cría)'),
        (AVE_TRASPATIO, 'Aves de Traspatio'),
        (MILPA, 'Milpa'),
        (ELAB_ALIMENTOS, 'Elaboración de Alimentos'),
        (ELAB_ARTESANIA, 'Elaboración de Artesanía'),
        (HERRAMIENTA, 'Herramientas y Equipo de Trabajo'),
        (OTRO, 'Otro, especificar')

    ]

    SALUD = 'SA'
    ALIMENTO = 'AL'
    TRABAJO = 'TR'
    EDUCACION = 'ED'
    FIESTAS = 'FI'
    MOTIVO_CREDITO_CHOICES = [
        (SALUD, 'Salud'),
        (ALIMENTO, 'Alimento'),
        (TRABAJO, 'Trabajo'),
        (EDUCACION, 'Educación'),
        (FIESTAS, 'Fiestas'),
        (OTRO, 'Otro, especificar')
    ]

    APROBADO = 'AP'
    REVISION = 'RV'
    RECHAZADO = 'RE'
    CANCELADO = 'CA'
    ESTATUS_S_CHOICES = [
        (APROBADO, 'Aprobado'),
        (REVISION, 'Revisión'),
        (RECHAZADO, 'Rechazado'),
        (CANCELADO, 'Cancelado')
    ]

    NEGOCIACION = 'NE'
    ESTATUS_E_CHOICES = [
        (APROBADO, 'Aprobado'),
        (REVISION, 'Revisión'),
        (NEGOCIACION, 'Negociación'),
        (CANCELADO, 'Cancelado')
    ]

    COBRADO = 'CO'
    ESTATUS_EJ_CHOICES = [
        (COBRADO, 'Cobrado'),
        (CANCELADO, 'Cancelado'),
        (REVISION, 'Revisión')
    ]

    folio_solicitud = models.AutoField(primary_key=True)
    clave_socio = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, blank=False, related_name='solicitud')
    fecha_solicitud = models.DateField(blank=False)
    tipo_credito = models.CharField(max_length=2, choices=TIPO_CREDITO_CHOICES, blank=False)
    act_productiva = models.CharField(max_length=2, choices=TIPO_ACTIV_PROD_CHOICES, blank=True)
    act_productiva_otro = models.CharField(max_length=40, blank=True, null=True)
    mot_credito = models.CharField(max_length=2, choices=MOTIVO_CREDITO_CHOICES, blank=False)
    mot_credito_otro = models.CharField(max_length=30, blank=True, null=True)
    emergencia_medica = models.BooleanField(default=False)
    # comprobante_medico = models.ImageField(blank=True)
    monto_solicitado = models.DecimalField(max_digits=9, decimal_places=2, blank=False)
    plazo_de_pago_solicitado = models.PositiveSmallIntegerField(blank=False)
    estatus_solicitud = models.CharField(max_length=2, choices=ESTATUS_S_CHOICES, blank=False)
    estatus_evaluacion = models.CharField(max_length=2, choices=ESTATUS_E_CHOICES, blank=False)
    estatus_ej_credito = models.CharField(max_length=2, choices=ESTATUS_EJ_CHOICES, blank=False)
    justificacion_credito = models.CharField(max_length=100, blank=True)
    comentarios_promotor = models.CharField(max_length=100, blank=True)
    comentarios_coordinador = models.CharField(max_length=100, blank=True)
    comentarios_gerente = models.CharField(max_length=100, blank=True)
    promotor = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, related_name='solic_promotor')
    coordinador = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True, related_name='solic_coord')
    pregunta_1 = models.BooleanField(default=False)
    pregunta_2 = models.BooleanField(default=False)
    pregunta_3 = models.BooleanField(default=False)
    pregunta_4 = models.BooleanField(default=False)
    irregularidades = models.CharField(max_length=100, blank=True)
    aval = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, blank=False, related_name='aval')
    familiar_responsable = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return '{0}- ({1}) ${2}'.format(self.folio_solicitud, self.clave_socio, self.monto_solicitado)
