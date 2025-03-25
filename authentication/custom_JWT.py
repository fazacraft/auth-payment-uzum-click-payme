from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User


class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = User

    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        return User.objects.filter(id=user_id).first()