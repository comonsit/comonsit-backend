# import datetime
#
# from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'url', 'username', 'first_name', 'last_name', 'clave_socio',
            'password', 'confirm_password', 'email', 'role', 'phone')

    # TODO: ADAPTAR PARA CREACIÓN DE SOCIOS
    # def create(self, validated_data):
    #     # invite_id = validated_data['invite_id']
    #     # del validated_data['invite_id']
    #     # user_invite = UserInvite.objects.get(uuid=invite_id)
    #     # validated_data['role'] = user_invite.user_type
    #     validated_data["password"] = make_password(validated_data["password"])
    #
    #     user = User.objects.create(**validated_data)
    #
    #     if user_invite.user_type == User.ROL_SOCIO:
    #         socio = Socio.objects.get(id=user_invite.company.id)
    #         socio.subs.add(user)
    #
    #     user_invite.delete()
    #     return user
#
# TODO: ADAPTAR PARA VALIDAR
#     def validate(self, data):
#         if data.get('password') != data.get('confirm_password'):
#             raise serializers.ValidationError({'password': "Those passwords don't match."})
#
#         password_validation.validate_password(data.get('password'))
#
#         del data['confirm_password']
#         return data


class UserChangePasswordSerializer(serializers.HyperlinkedModelSerializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'old_password',
                  'password', 'confirm_password', 'email', 'role', 'phone')
        read_only_fields = ('url', 'username')

    def update(self, instance, validated_data):
        if validated_data.get('password', False):
            instance.set_password(validated_data["password"])
        instance.role = validated_data.get('role', instance.role)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance

    def validate(self, data):
        if data.get('old_password', False) and not self.instance.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'password': "Those passwords don't match."})

        if data.get('password', False):
            password_validation.validate_password(data.get('password'))

        return data
