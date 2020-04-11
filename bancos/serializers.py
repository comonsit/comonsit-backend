from rest_framework import serializers
from .models import ConceptoBanco, SubCuenta, MovimientoBanco


class SubCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCuenta
        fields = "__all__"


class ConceptoBancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoBanco
        fields = "__all__"


class MovimientoBancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoBanco
        fields = "__all__"
