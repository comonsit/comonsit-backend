# from unittest import skip
import datetime
import json
from django.urls import reverse
from rest_framework.views import status

from .models import SolicitudCredito
from socios.tests import SocioBaseAPITestCase
from comonSitDjango.constants import CAFE


SOLICITUDES_LIST = reverse('api:solic-creditos-list')


class SolicitudCreationTestCase(SocioBaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.solicitud = self.create_solicitud(datetime.datetime.today())

    def create_solicitud(self, date):
        solicitud = SolicitudCredito.objects.create(clave_socio=self.productora,
                                                    fecha_solicitud=date,
                                                    proceso=CAFE,
                                                    tipo_credito=SolicitudCredito.MICROCREDITO,
                                                    emergencia_medica=False,
                                                    monto_solicitado=800,
                                                    plazo_de_pago_solicitado=3,
                                                    justificacion_credito="justificación",
                                                    aval=self.socio,
                                                    familiar_responsable="Nombre Familiar",
                                                    promotor=self.user)
        solicitud.save()
        return solicitud

    def test_solicitud_creation(self):
        solicitud_data = {
            "clave_socio": self.productora.clave_socio,
            "fecha_solicitud": "2021-02-16",
            "proceso": CAFE,
            "tipo_credito": SolicitudCredito.MICROCREDITO,
            "act_productiva": SolicitudCredito.CAFETAL,
            "act_productiva_otro": "",
            "mot_credito": SolicitudCredito.TRABAJO,
            "mot_credito_otro": "",
            "emergencia_medica": False,
            "monto_solicitado": 500,
            "plazo_de_pago_solicitado": 2,
            "justificacion_credito": "...",
            "comentarios_promotor": "Todo revisado",
            "aval": self.socio.clave_socio,
            "familiar_responsable": "madrev",
            "chat": [{"comentario": "Enviando Solicitud"}]
        }

        response = self.client.post(SOLICITUDES_LIST,
                                    json.dumps(solicitud_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        solicitud_1_id = json.loads(response.content)['folio_solicitud']
        self.solicitud_1 = SolicitudCredito.objects.get(folio_solicitud=solicitud_1_id)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_mesa_control(self):
        """
        Test create a new Solicitud
        """
        solicitud_data = {
          "pregunta_1": True,
          "pregunta_2": True,
          "pregunta_3": True,
          "pregunta_4": True,
          "estatus_solicitud": SolicitudCredito.APROBADO,
          "comentarios_coordinador": "...",
          "chat": [{"comentario": "Aprobado"}]
        }
        patch_url = SOLICITUDES_LIST + str(self.solicitud.folio_solicitud) + '/'
        response = self.client.patch(patch_url,
                                     json.dumps(solicitud_data),
                                     content_type='application/json',
                                     HTTP_AUTHORIZATION=self.token_coord)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_evaluacion(self):
        """
        Test create a new Solicitud
        """
        solicitud_data = {
          "monto_aprobado": 500,
          "plazo_aprobado": 3,
          "tasa_aprobada": 4,
          "tasa_mor_aprobada": 1,
          "comentarios_gerente": "Aprobado solo 500",
          "estatus_evaluacion": SolicitudCredito.APROBADO,
          "chat": [{"comentario": "Aprobado"}]
        }
        patch_url = SOLICITUDES_LIST + str(self.solicitud.folio_solicitud) + '/'
        response = self.client.patch(patch_url,
                                     json.dumps(solicitud_data),
                                     content_type='application/json',
                                     HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
