# from unittest import skip
import datetime
import json
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from rest_framework.views import status

from contratos.tests import ContratoActivationTestCase, CONTRATOS_LIST
from contratos.models import ContratoCredito

PAGOS_LIST = reverse('api:pagos-list')


class PagoTestCases(ContratoActivationTestCase):
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
        new_status = json.loads(response.content)['estatus_nuevo']
        self.assertEqual(new_status, ContratoCredito.VENCIDO)

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

    def test_pay_all_debt(self):
        """
        CASO 2: Pay all debt
        """
        c_date = datetime.datetime.today() - relativedelta(months=4)
        contrato = self.create_contrato(fecha_inicio=c_date,
                                        monto=100,
                                        plazo=1,
                                        estatus_ejecucion=ContratoCredito.COBRADO)
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": datetime.datetime.today().strftime("%Y-%m-%d"),
          "cantidad": 119,
          "abono_capital": 100,
          "interes_ord": 16,
          "interes_mor": 3
        }
        # print(f'c_date {c_date}')
        # print(f'date of todays payment {datetime.datetime.today()}')
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_status = json.loads(response.content)['estatus_nuevo']
        self.assertEqual(new_status, ContratoCredito.PAGADO)

    def test_pay_partials(self):
        """
        CASO 3: Make various small payments
        """
        c_date = datetime.datetime.today() - relativedelta(months=8)
        # print(f'fecha inicio {c_date}')
        contrato = self.create_contrato(fecha_inicio=c_date,
                                        monto=1000,
                                        plazo=3,
                                        estatus_ejecucion=ContratoCredito.COBRADO)
        """
        PAYMENT 1
        1 month after
        Abono a intereses
        """
        payment_1_date = c_date + relativedelta(months=1)
        # print(f'payment_1_date {payment_1_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_1_date.strftime("%Y-%m-%d"),
          "cantidad": 40,
          "abono_capital": 0,
          "interes_ord": 40,
          "interes_mor": 0
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_status = json.loads(response.content)['estatus_nuevo']
        prev_debt = json.loads(response.content)['deuda_prev_total']
        prev_debt_ord = json.loads(response.content)['deuda_prev_int_ord']
        self.assertEqual(new_status, ContratoCredito.VIGENTE)
        self.assertEqual(prev_debt, '1040.00')
        self.assertEqual(prev_debt_ord, '40.00')

        """
        PAYMENT 2
        3 month after
        Abono a intereses y capital
        """
        payment_2_date = c_date + relativedelta(months=3)+relativedelta(days=1)
        # print(f'payment_2_date {payment_2_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_2_date.strftime("%Y-%m-%d"),
          "cantidad": 180,
          "abono_capital": 100,
          "interes_ord": 80,
          "interes_mor": 0
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_status = json.loads(response.content)['estatus_nuevo']
        prev_debt = json.loads(response.content)['deuda_prev_total']
        prev_debt_ord = json.loads(response.content)['deuda_prev_int_ord']
        self.assertEqual(new_status, ContratoCredito.VENCIDO)
        self.assertEqual(prev_debt, '1080.00')
        self.assertEqual(prev_debt_ord, '80.00')

        """
        PAYMENT 3
        4 month after
        Abono a intereses ord, mor y capital
        """
        payment_3_date = c_date + relativedelta(months=4)
        # print(f'payment_3_date {payment_3_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_3_date.strftime("%Y-%m-%d"),
          "cantidad": 140,
          "abono_capital": 100,
          "interes_ord": 40,
          "interes_mor": 0
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_status = json.loads(response.content)['estatus_nuevo']
        prev_debt = json.loads(response.content)['deuda_prev_total']
        prev_debt_ord = json.loads(response.content)['deuda_prev_int_ord']
        prev_debt_mor = json.loads(response.content)['deuda_prev_int_mor']
        self.assertEqual(new_status, ContratoCredito.VENCIDO)
        self.assertEqual(prev_debt, '950.00')
        self.assertEqual(prev_debt_ord, '40.00')
        self.assertEqual(prev_debt_mor, '10.00')

        """
        Verify that debt can be calculated for moments before payments
        """
        debt_date = c_date + relativedelta(months=3) + relativedelta(days=3)
        deuda_url = CONTRATOS_LIST + str(contrato.id) + "/deuda/?fecha=" + debt_date.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        current_status = json.loads(response.content)['estatus_detail']
        prev_debt = json.loads(response.content)['total_deuda']
        prev_debt_ord = json.loads(response.content)['interes_ordinario_deuda']
        self.assertEqual(current_status, ContratoCredito.VENCIDO)
        self.assertEqual(prev_debt, 900)
        self.assertEqual(prev_debt_ord, 0)

        """
        PAYMENT 4
        8 month after
        Pay Everything to completion
        """
        payment_4_date = datetime.datetime.today()
        # print(f'payment_4_date {payment_4_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_4_date.strftime("%Y-%m-%d"),
          "cantidad": 1010,
          "abono_capital": 800,
          "interes_ord": 160,
          "interes_mor": 50
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_status = json.loads(response.content)['estatus_nuevo']
        prev_debt = json.loads(response.content)['deuda_prev_total']
        prev_debt_ord = json.loads(response.content)['deuda_prev_int_ord']
        prev_debt_mor = json.loads(response.content)['deuda_prev_int_mor']
        self.assertEqual(new_status, ContratoCredito.PAGADO)
        self.assertEqual(prev_debt, '1010.00')
        self.assertEqual(prev_debt_ord, '160.00')
        self.assertEqual(prev_debt_mor, '50.00')

    def test_payment_unordered(self):
        """
        Unordered payment
        """
        c_date = datetime.datetime.today() - relativedelta(months=2)
        # print(f'fecha inicio {c_date}')
        contrato = self.create_contrato(fecha_inicio=c_date,
                                        monto=100,
                                        plazo=3,
                                        estatus_ejecucion=ContratoCredito.COBRADO)
        """
        PAYMENT 1 - REGULAR
        1 month after
        """
        payment_1_date = c_date + relativedelta(months=1)
        # print(f'payment_1_date {payment_1_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_1_date.strftime("%Y-%m-%d"),
          "cantidad": 50,
          "abono_capital": 50,
          "interes_ord": 0,
          "interes_mor": 0
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        """
        PAYMENT 2 - OUT OF ORDER
        5 days after start
        Expected failure
        """
        payment_2_date = c_date + relativedelta(days=5)
        # print(f'payment_2_date {payment_2_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_2_date.strftime("%Y-%m-%d"),
          "cantidad": 10,
          "abono_capital": 10,
          "interes_ord": 0,
          "interes_mor": 0
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        error_messages = json.loads(response.content)
        self.assertTrue('fecha_pago' in error_messages, True)

    def test_payments_with_variable_interest_rate(self):
        """
        CASO 4: Tasa VARIABLE
        """
        c_date = datetime.datetime(2020, 12, 1)
        # print(f'fecha inicio {c_date}')
        contrato = self.create_contrato(fecha_inicio=c_date,
                                        monto=5000,
                                        plazo=2,
                                        tipo_tasa=ContratoCredito.VARIABLE,
                                        estatus_ejecucion=ContratoCredito.COBRADO)

        # deuda = json.loads(response.content)['total_deuda']
        # moratorio = json.loads(response.content)['interes_moratorio_deuda']
        # abonado = json.loads(response.content)['capital_abonado']
        # ordinario = json.loads(response.content)['interes_ordinario_deuda']
        # status_contrato = json.loads(response.content)['estatus_detail']
        # self.assertEqual(deuda, 500)
        # self.assertEqual(ordinario, 0)
        # self.assertEqual(moratorio, 0)
        # self.assertEqual(abonado, 0)
        # self.assertEqual(status_contrato, ContratoCredito.VIGENTE)

        """
        PAYMENT 1
        5 days after
        """
        payment_1_date = c_date + relativedelta(days=5)
        # print(f'payment_1_date {payment_1_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_1_date.strftime("%Y-%m-%d"),
          "cantidad": "1032.87",
          "abono_capital": 1000,
          "interes_ord": "32.87",
          "interes_mor": 0
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # print(response.content)
        # print('\n')
        new_status = json.loads(response.content)['estatus_nuevo']
        prev_debt = json.loads(response.content)['deuda_prev_total']
        prev_debt_ord = json.loads(response.content)['deuda_prev_int_ord']
        self.assertEqual(new_status, ContratoCredito.VIGENTE)
        self.assertEqual(prev_debt, '5032.87')
        self.assertEqual(prev_debt_ord, '32.87')
        #
        """
        Check Debt
        """
        debt_1_date = c_date + relativedelta(days=5)
        # print(f'debt_1_date {debt_1_date}')
        deuda_url = CONTRATOS_LIST + str(contrato.id) + "/deuda/?fecha=" + debt_1_date.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        new_status = json.loads(response.content)['estatus_detail']
        prev_debt = json.loads(response.content)['total_deuda']
        prev_debt_ord = json.loads(response.content)['interes_ordinario_deuda']
        # print(response.content)
        self.assertEqual(new_status, ContratoCredito.VIGENTE)
        self.assertEqual(prev_debt, 4000)
        self.assertEqual(prev_debt_ord, 0)

        """
        PAYMENT 2
        40 days after
        """
        payment_2_date = c_date + relativedelta(days=40)
        # print(f'payment_2_date {payment_2_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_2_date.strftime("%Y-%m-%d"),
          "cantidad": "84.1",
          "abono_capital": 0,
          "interes_ord": "84.1",
          "interes_mor": 0
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # print(response.content)
        # print('\n')
        new_status = json.loads(response.content)['estatus_nuevo']
        prev_debt = json.loads(response.content)['deuda_prev_total']
        prev_debt_ord = json.loads(response.content)['deuda_prev_int_ord']
        self.assertEqual(new_status, ContratoCredito.VIGENTE)
        self.assertEqual(prev_debt, '4184.10')
        self.assertEqual(prev_debt_ord, '184.10')

        """
        Check Debt
        """
        debt_2_date = c_date + relativedelta(days=40)
        # print(f'debt_2_date {debt_2_date}')
        deuda_url = CONTRATOS_LIST + str(contrato.id) + "/deuda/?fecha=" + debt_2_date.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        new_status = json.loads(response.content)['estatus_detail']
        prev_debt = json.loads(response.content)['total_deuda']
        prev_debt_ord = json.loads(response.content)['interes_ordinario_deuda']
        self.assertEqual(new_status, ContratoCredito.VIGENTE)
        # print(response.content)
        self.assertEqual(prev_debt, 4100)
        self.assertEqual(prev_debt_ord, 100)

        """
        Check Debt DUE DATE
        """
        debt_3_date = datetime.datetime(2021, 2, 1)
        # print(f'debt_3_date {debt_3_date}')
        deuda_url = CONTRATOS_LIST + str(contrato.id) + "/deuda/?fecha=" + debt_3_date.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        new_status = json.loads(response.content)['estatus_detail']
        prev_debt = json.loads(response.content)['total_deuda']
        prev_debt_ord = json.loads(response.content)['interes_ordinario_deuda']
        prev_debt_mor = json.loads(response.content)['interes_moratorio_deuda']
        # TODO: add when vigencia error is corrected
        # self.assertEqual(new_status, ContratoCredito.VENCIDO)
        # print(response.content)
        self.assertEqual(prev_debt, 4215.72)
        self.assertEqual(prev_debt_ord, 215.72)
        self.assertEqual(prev_debt_mor, 0)

        """
        PAYMENT 3
        70 days after
        """
        payment_3_date = c_date + relativedelta(days=70)
        # print(f'payment_3_date {payment_3_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_3_date.strftime("%Y-%m-%d"),
          "cantidad": 3268.32,
          "abono_capital": 3000,
          "interes_ord": "257.8",
          "interes_mor": "10.52"
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_status = json.loads(response.content)['estatus_nuevo']
        prev_debt = json.loads(response.content)['deuda_prev_total']
        prev_debt_ord = json.loads(response.content)['deuda_prev_int_ord']
        prev_debt_mor = json.loads(response.content)['deuda_prev_int_mor']
        self.assertEqual(new_status, ContratoCredito.VENCIDO)
        self.assertEqual(prev_debt, "4268.32")
        self.assertEqual(prev_debt_ord, "257.80")
        self.assertEqual(prev_debt_mor, "10.52")
        deuda_url = CONTRATOS_LIST + str(contrato.id) + "/deuda/?fecha=" + payment_3_date.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        """
        DAY 45
        Verify that debt can be calculated for moments before payments
        """
        debt_4_date = c_date + relativedelta(days=45)
        # print(f'debt_4_date {debt_4_date}')
        deuda_url = CONTRATOS_LIST + str(contrato.id) + "/deuda/?fecha=" + debt_4_date.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        new_status = json.loads(response.content)['estatus_detail']
        prev_debt = json.loads(response.content)['total_deuda']
        prev_debt_ord = json.loads(response.content)['interes_ordinario_deuda']
        prev_debt_mor = json.loads(response.content)['interes_moratorio_deuda']
        # print(response.content)
        self.assertEqual(new_status, ContratoCredito.VIGENTE)
        self.assertEqual(prev_debt, 4126.3)
        self.assertEqual(prev_debt_ord, 126.3)
        self.assertEqual(prev_debt_mor, 0)
        """
        DAY 65
        Verify that debt can be calculated for moments before payments
        """
        debt_5_date = c_date + relativedelta(days=65)
        # print(f'debt_5_date {debt_5_date}')
        deuda_url = CONTRATOS_LIST + str(contrato.id) + "/deuda/?fecha=" + debt_5_date.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        new_status = json.loads(response.content)['estatus_detail']
        prev_debt = json.loads(response.content)['total_deuda']
        prev_debt_ord = json.loads(response.content)['interes_ordinario_deuda']
        prev_debt_mor = json.loads(response.content)['interes_moratorio_deuda']
        # print(response.content)
        self.assertEqual(new_status, ContratoCredito.VENCIDO)
        self.assertEqual(prev_debt, 4235.45)
        self.assertEqual(prev_debt_ord, 231.5)
        self.assertEqual(prev_debt_mor, 3.94)

        """
        PAYMENT 4 - FINAL PAYMENT
        80 days after
        """
        payment_4_date = c_date + relativedelta(days=80)
        # print(f'payment_4_date {payment_4_date}')
        pago_data = {
          "credito": contrato.id,
          "fecha_pago": payment_4_date.strftime("%Y-%m-%d"),
          "cantidad": "1016.43",
          "abono_capital": 1000,
          "interes_ord": "13.15",
          "interes_mor": "3.28"
        }
        response = self.client.post(PAGOS_LIST,
                                    json.dumps(pago_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_status = json.loads(response.content)['estatus_nuevo']
        prev_debt = json.loads(response.content)['deuda_prev_total']
        prev_debt_ord = json.loads(response.content)['deuda_prev_int_ord']
        prev_debt_mor = json.loads(response.content)['deuda_prev_int_mor']
        self.assertEqual(new_status, ContratoCredito.PAGADO)
        self.assertEqual(prev_debt, '1016.43')
        self.assertEqual(prev_debt_ord, '13.15')
        self.assertEqual(prev_debt_mor, '3.28')

        """
        DAY 81
        Verify debt is payed
        """
        debt_6_date = c_date + relativedelta(days=81)
        # print(f'debt_6_date {debt_6_date}')
        deuda_url = CONTRATOS_LIST + str(contrato.id) + "/deuda/?fecha=" + debt_6_date.strftime("%Y-%m-%d")
        response = self.client.get(deuda_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        current_status = json.loads(response.content)['estatus_detail']
        self.assertEqual(current_status, ContratoCredito.PAGADO)
