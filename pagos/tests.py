# from unittest import skip
import datetime
import json
from django.urls import reverse
from rest_framework.views import status

from contratos.tests import ContratoActivationTestCase

PAGOS_LIST = reverse('api:pagos-list')


class PagoTestCase(ContratoActivationTestCase):
    def setUp(self):
        super().setUp()

    def test_pago(self):
        pago_data = {
          "credito": self.contrato.id,
          "fecha_pago": datetime.datetime.today().strftime("%Y-%m-%d"),
          "cantidad": 100,
          "abono_capital": 0,
          "interes_ord": 100,
          "interes_mor": 0
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_pago_failure(self):
        pago_data = {
          "credito": self.contrato.id,
          "fecha_pago": datetime.datetime.today().strftime("%Y-%m-%d"),
          "cantidad": 100,
          "abono_capital": 0,
          "interes_ord": 0,
          "interes_mor": 100
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        response_error = json.loads(response.content)['interes_mor']
        expected_error = [("El pago 100.00 es mayor a"
                           " lo que se debe de interés moratorio 10.00")]
        self.assertEqual(response_error, expected_error)
