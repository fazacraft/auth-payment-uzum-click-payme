import uuid

from django.contrib.auth.hashers import make_password
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
            'password' : {'write_only': True },
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        update_fields = []
        full_name = validated_data.get('full_name')
        password = validated_data.get('password')
        if full_name:
            instance.full_name = full_name
            update_fields.append('full_name')
        if password:
            instance.password = make_password(password)
            update_fields.append('password')
        instance.save(update_fields = update_fields)

        return instance




class OTPSerializer(serializers.Serializer):
    otp_key = serializers.UUIDField(default=uuid.uuid4)
    otp_code = serializers.IntegerField(min_value=1000, max_value=9999)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()