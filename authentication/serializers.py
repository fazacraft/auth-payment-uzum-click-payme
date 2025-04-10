import uuid

from django.contrib.auth.hashers import make_password
from django.db.models import CharField
from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'email',
            'role',
            'password',
        )

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class UserUpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()



class OTPSerializer(serializers.Serializer):
    otp_key = serializers.UUIDField(default=uuid.uuid4)
    otp_code = serializers.IntegerField(min_value=1000, max_value=9999)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
