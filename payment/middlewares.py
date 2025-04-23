import base64

from rest_framework import status
from rest_framework.response import Response

from config import settings
from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException


class PaymeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/payme/'):
            try:
                auth = request.headers.get('Authorization')
                if not auth or not auth.startswith('Basic '):
                    raise CustomApiException(ErrorCodes.UNAUTHORIZED)

                encoded = auth.split(' ')[1]
                decoded = base64.b64decode(encoded).decode()
                login, password = decoded.split(':')

                if login != settings.PAYME_LOGIN or password != settings.PAYME_PASSWORD:
                    return Response(
                        data={
                            'code': -32504,
                            'message': {
                                'uz': 'Avtorizatsiya yaroqsiz',
                                'ru': 'Авторизация недействительна',
                                'en': 'Authorization invalid',
                            },
                        },
                        status=status.HTTP_200_OK
                    )

            except Exception:
                return Response(
                    data={
                        'code': -32504,
                        'message': {
                            'uz': 'Xatolik yuz berdi',
                            'ru': 'Произошла ошибка',
                            'en': 'An error occurred',
                        },
                    },
                    status=status.HTTP_200_OK
                )

        return self.get_response(request)
