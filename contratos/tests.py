# from unittest import skip
import datetime
from unittest import skip
from dateutil.relativedelta import relativedelta
import json
from django.urls import reverse
from rest_framework.views import status

from solicitudes.models import SolicitudCredito
from .models import ContratoCredito
from solicitudes.tests import SolicitudCreationTestCase, SOLICITUDES_LIST

CONTRATOS_LIST = reverse('api:contratos-list')


class ContratoActivationTestCase(SolicitudCreationTestCase):
    """
    CASO 1: Check debt at different times
    """

    def setUp(self):
        super().setUp()
        self.contrato_date = datetime.datetime.today() - relativedelta(months=5)
        self.contrato = self.create_contrato(fecha_inicio=self.contrato_date, estatus_ejecucion=ContratoCredito.COBRADO)

    def create_contrato(
        self, fecha_inicio=datetime.datetime.today(), monto=500, plazo=3,
        tipo_tasa=ContratoCredito.FIJA, estatus_ejecucion=None
    ):
        solicitud = self.create_solicitud(fecha_inicio)
        solicitud_data = {
          "monto_aprobado": monto,
          "plazo_aprobado": plazo,
          "tasa_aprobada": 4,
          "tasa_mor_aprobada": 1,
          "comentarios_gerente": "Aprobado solo 500",
          "estatus_evaluacion": SolicitudCredito.APROBADO,
          "chat": [{"comentario": "Aprobado"}]
        }
        patch_url = SOLICITUDES_LIST + str(solicitud.folio_solicitud) + '/'
        response = self.client.patch(patch_url,
                                     json.dumps(solicitud_data),
                                     content_type='application/json',
                                     HTTP_AUTHORIZATION=self.token)
        contrato = ContratoCredito.objects.get(pk=response.data['contrato'])
        if estatus_ejecucion == ContratoCredito.COBRADO:
            contrato.fecha_inicio = fecha_inicio
            contrato.tipo_tasa = ContratoCredito.FIJA
            contrato.estatus_ejecucion = ContratoCredito.COBRADO
            contrato.save()
        return contrato

    def test_contrato_activation(self):
        contrato = self.create_contrato()
        contrato_data = {
          "fecha_inicio": self.contrato_date.strftime("%Y-%m-%d"),
          "tipo_tasa": ContratoCredito.FIJA,
          "estatus_ejecucion": ContratoCredito.COBRADO
        }
        contrato_url = CONTRATOS_LIST + str(contrato.id) + '/'
        response = self.client.patch(contrato_url,
                                     json.dumps(contrato_data),
                                     content_type='application/json',
                                     HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_deuda_day_before_start(self):
        day_before_start = self.contrato.fecha_inicio - relativedelta(days=1)
        # print(f'Day Before = {day_before_start}')
        # print(f'Fecha Inicio = {self.contrato.fecha_inicio}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + day_before_start.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        response_error = json.loads(response.content)['non_field_errors']
        expected_error = f"La fecha {day_before_start.strftime('%d %b %Y')} es previa al" \
                         f" inicio del crédito {self.contrato.fecha_inicio.strftime('%d %b %Y')}"
        self.assertEqual(response_error, expected_error)
        # print('el otro')
        # print(self.contrato.fecha_vencimiento())

    def test_deuda_same_day_start(self):
        day_after_start = self.contrato.fecha_inicio
        # print(f'Day After = {day_after_start}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + day_after_start.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        status_contrato = json.loads(response.content)['estatus_detail']
        self.assertEqual(deuda, 500)
        self.assertEqual(ordinario, 0)
        self.assertEqual(moratorio, 0)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VIGENTE)

    def test_deuda_day_after(self):
        day_after_start = self.contrato.fecha_inicio + relativedelta(days=1)
        # # print(f'Fecha Inicio = {self.contrato.fecha_inicio}')
        # print(f'Day After = {day_after_start}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + day_after_start.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        status_contrato = json.loads(response.content)['estatus_detail']
        self.assertEqual(deuda, 500)
        self.assertEqual(ordinario, 0)
        self.assertEqual(moratorio, 0)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VIGENTE)

    def test_deuda_one_monthish_after_start(self):
        monthish_after = self.contrato.fecha_inicio + relativedelta(days=35)
        # print(f'monthish_after = {monthish_after}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + monthish_after.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        status_contrato = json.loads(response.content)['estatus_detail']
        self.assertEqual(deuda, 520)
        self.assertEqual(ordinario, 20)
        self.assertEqual(moratorio, 0)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VIGENTE)

    def test_deuda_two_monthish_after_start(self):
        two_monthish_after = self.contrato.fecha_inicio + relativedelta(days=65)
        # print(f'two_monthish_after = {two_monthish_after}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + two_monthish_after.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        status_contrato = json.loads(response.content)['estatus_detail']
        self.assertEqual(deuda, 540)
        self.assertEqual(ordinario, 40)
        self.assertEqual(moratorio, 0)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VIGENTE)

    """
    FIX!!
    """
    @skip("Pending deuda status is fixed")
    def test_deuda_fecha_vencimiento(self):
        three_months = self.contrato.fecha_inicio + relativedelta(months=3)
        # print(f'three_months = {three_months}')
        # print(f'Fecha Vencimiento = {self.contrato.fecha_vencimiento()}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + three_months.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        status_contrato = json.loads(response.content)['estatus_detail']
        self.assertEqual(deuda, 560)
        self.assertEqual(ordinario, 60)
        self.assertEqual(moratorio, 0)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VENCIDO)

    def test_deuda_three_months_after_start_plus_one(self):
        three_months = self.contrato.fecha_inicio + relativedelta(months=3)+relativedelta(days=1)
        # print(f'three_months +1 = {three_months}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + three_months.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        status_contrato = json.loads(response.content)['estatus_detail']
        self.assertEqual(deuda, 560)
        self.assertEqual(ordinario, 60)
        self.assertEqual(moratorio, 0)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VENCIDO)

    def test_deuda_100days_after(self):
        hundred_days = self.contrato.fecha_inicio + relativedelta(days=100)
        # print(f'hundred_days = {hundred_days}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + hundred_days.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        status_contrato = json.loads(response.content)['estatus_detail']
        self.assertEqual(deuda, 560)
        self.assertEqual(ordinario, 60)
        self.assertEqual(moratorio, 0)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VENCIDO)

    def test_deuda_four_months_after_start(self):
        four_months = self.contrato.fecha_inicio + relativedelta(months=4)
        # print(f'four_months = {four_months}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/?fecha=" + four_months.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        status_contrato = json.loads(response.content)['estatus_detail']
        # # print(response.content)
        self.assertEqual(deuda, 585)
        self.assertEqual(ordinario, 80)
        self.assertEqual(moratorio, 5)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VENCIDO)

    def test_deuda_today(self):
        # print(f'Today = {datetime.datetime.today()}')
        deuda_url = CONTRATOS_LIST + str(self.contrato.id) + "/deuda/"
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        deuda = json.loads(response.content)['total_deuda']
        moratorio = json.loads(response.content)['interes_moratorio_deuda']
        abonado = json.loads(response.content)['capital_abonado']
        ordinario = json.loads(response.content)['interes_ordinario_deuda']
        status_contrato = json.loads(response.content)['estatus_detail']
        # # print(response.content)
        self.assertEqual(deuda, 610)
        self.assertEqual(ordinario, 100)
        self.assertEqual(moratorio, 10)
        self.assertEqual(abonado, 0)
        self.assertEqual(status_contrato, ContratoCredito.VENCIDO)
