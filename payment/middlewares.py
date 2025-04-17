import base64
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
                    raise CustomApiException(ErrorCodes.UNAUTHORIZED)

            except Exception:
                raise CustomApiException(ErrorCodes.UNAUTHORIZED)


        response = self.get_response(request)
        return response
