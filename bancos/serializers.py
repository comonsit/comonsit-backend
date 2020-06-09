from rest_framework import serializers
from .models import Banco, SubCuenta, MovimientoBanco, RegistroContable


class BancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banco
        fields = "__all__"


class SubCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCuenta
        fields = "__all__"


class MovimientoBancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoBanco
        fields = "__all__"


class RegistroContableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroContable
        fields = "__all__"
