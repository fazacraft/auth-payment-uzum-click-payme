from django.http import JsonResponse
from Uzum.const.errors import UzumErrors
from Uzum.utils import check_auth


class UzumMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/payment/uzum/' in request.path:
            print(request.headers)
            value  = request.headers.get('Authorization')

            if not check_auth(value):
                return JsonResponse(
                    data={
                        'errorCode': UzumErrors.AccessDenied.value,
                    },
                    status=400
                )

        response = self.get_response(request)
        return response

