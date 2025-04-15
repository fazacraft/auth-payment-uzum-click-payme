import time

from django.http import JsonResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from authentication.utils import user_login


class RequestLogginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        print(f"Incoming request: {request.method} {request.path}")
        if not self.is_allowed(request):
            return JsonResponse(
                data={
                    'result': f'Not Allowed this urls {request.path}',
                    'ok': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        response = self.get_response(request)

        duration = time.time() - start_time
        response['X-Process_Time'] = f"{duration:.3f}s"
        print(f'Processed in {duration:.3f} seconds')

        return response

    @staticmethod
    def is_allowed(request):
        allowed_urls=[
            reverse('user_login'),
            reverse('user_create'),
            reverse('payment'),
        ]
        if request.path in allowed_urls:
            return True
        static_allowed_urls=[
            '/admin/',
            '/swagger/',
        ]
        if any(request.path.startswith(url) for url in static_allowed_urls):
            return True


        return False
