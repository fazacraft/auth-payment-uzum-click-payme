from rest_framework import status
from rest_framework.response import Response

from Uzum.const.errors import UzumErrors
from Uzum.utils import check_auth


class UzumMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('payment/uzum/'):
            value  = request.headers.get('Authorization')

            if not check_auth(value):
                return Response(
                    data={
                        'errorCode': UzumErrors.AccessDenied.value,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        response = self.get_response(request)
        return response

