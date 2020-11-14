from django.test import TestCase
from .models import Cargo


class CargoTestCase(TestCase):
    def setUp(self):
        Cargo.objects.create(nombre_de_cargo="Tatik")

    def test_testing(self):
        """Cargos that can speak are correctly identified"""
        jwan = Cargo.objects.get(nombre_de_cargo="Tatik")
        self.assertEqual(jwan.nombre_de_cargo, 'Tatik')
