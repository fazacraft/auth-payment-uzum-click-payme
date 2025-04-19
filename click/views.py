from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from click.errors import ClickErrorCodes
from click.serializers import PrepareSerializer


# Create your views here.


class ClickViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=PrepareSerializer,
        tags=['Click']
    )
    def prepare(self,request):
        serializer = PrepareSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'error': ClickErrorCodes.ErrorInRequestFromClick,
                    'error_note':' somsaada bayram'
                },
                status=status.HTTP_200_OK
            )
        return 1

