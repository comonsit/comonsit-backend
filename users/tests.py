import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from tsumbalil.models import Region, Comunidad
from socios.models import Socio
from comonSitDjango.constants import ACTIVO, NO_PARTICIPA
from .models import User


API_TOKEN_LOGIN = reverse('token_obtain_pair')
API_TOKEN_REFRESH = reverse('token_refresh')
USER_ME = reverse('api:user-list') + 'me/'


class UserTokenLoginAPITestCase(APITestCase):
    def setUp(self):
        self.username = "jwan"
        self.email = "jwan@snow.com"
        self.password = "chawu"
        self.role = User.ROL_GERENTE
        self.clave_socio = 1
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.role = self.role
        # self.user.clave_socio = self.clave_socio

    def test_authentication_without_password(self):
        """
        Try to authenticate without password
        """
        response = self.client.post(API_TOKEN_LOGIN, {"username": "snowman"})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_authentication_with_wrong_password(self):
        """
        Try to authenticate with wrong password
        """
        response = self.client.post(API_TOKEN_LOGIN, {"username": self.username, "password": "I_know"})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_authentication_with_valid_data(self):
        """
        Authenticate with valid credentials
        """
        response = self.client.post(API_TOKEN_LOGIN, {"username": self.username, "password": self.password})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.assertTrue("refresh" in json.loads(response.content))

    def test_token_refresh(self):
        """
        Refresh jwt token
        """
        self.token = json.loads(self.client.post(API_TOKEN_LOGIN,
                                             {"username": self.username, "password": self.password}).content)['refresh']
        response = self.client.post(API_TOKEN_REFRESH, {"refresh": self.token})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue("access" in json.loads(response.content))


class UserBaseAPITestCase(APITestCase):
    def setUp(self):
        self.username = "jwan"
        self.email = "jwan@snow.com"
        self.password = "chawu"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        # self.user.clave_socio = self.clave_socio

        self.user.first_name = "Jwan"
        self.user.last_name = "Lopez"
        self.user.role = User.ROL_GERENTE
        self.user.phone = "9196531234"
        self.token = self.api_token_authentication(self.username, self.password)

        self.region = Region.objects.create(nombre_de_region="Chilum")
        self.comunidad = Comunidad.objects.create(
            nombre_de_comunidad="Chilum Centro",
            region=self.region
        )

        self.socio = Socio.objects.create(
            nombres=self.user.first_name,
            apellido_paterno=self.user.last_name,
            comunidad=self.comunidad,
            genero=Socio.MASCULINO,
            estatus_cafe=ACTIVO,
            estatus_miel=NO_PARTICIPA,
            estatus_yip=NO_PARTICIPA,
            estatus_trabajador=NO_PARTICIPA,
            estatus_comonSit=ACTIVO,
        )
        self.user.clave_socio = self.socio

        self.user.save()

    def api_token_authentication(self, username, password):
        return "Bearer {0}".format(json.loads(self.client.post(API_TOKEN_LOGIN,
                                             {"username": username, "password": password}).content)['access'])
