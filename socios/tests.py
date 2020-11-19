# from unittest import skip
from django.urls import reverse
from rest_framework.views import status

from .models import Socio
from users.tests import UserBaseAPITestCase
from comonSitDjango.constants import ACTIVO, NO_PARTICIPA


SOCIOS_LIST = reverse('api:socios-list')


class SocioCreationTestCase(UserBaseAPITestCase):
    def test_socio_creation(self):
        """
        Test create a new socio
        """
        socio_data = {
            "nombres": "Jwan",
            "apellido_paterno": "Lopez",
            "genero": Socio.MASCULINO,
            "comunidad": self.comunidad.id,
            "estatus_cafe": ACTIVO,
            "estatus_miel": NO_PARTICIPA,
            "estatus_yip": NO_PARTICIPA,
            "estatus_trabajador": NO_PARTICIPA,
            "estatus_comonSit": ACTIVO,
        }
        response = self.client.post(SOCIOS_LIST, HTTP_AUTHORIZATION=self.token, data=socio_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class SocioReadTestCase(UserBaseAPITestCase):
    def test_socio_read(self):
        """
        Test read socios list
        """
        response = self.client.get(SOCIOS_LIST, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
