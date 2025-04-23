import base64
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response

from Uzum.const.errors import UzumErrors
from config.settings import UZUM_LOGIN, UZUM_PASSWORD, UZUM_SERVICE_ID
from payment.utils import reconvert_to_ms

test_string = str(UZUM_LOGIN) + ':' + str(UZUM_PASSWORD)


def encode(test_string):
    encoded = base64.b64encode(test_string.encode())
    return encoded


def check_auth(testbek):
    qyu = testbek.split()[1]
    return qyu == encode(test_string)


def check_service_id(service_id):
    return UZUM_SERVICE_ID == service_id


def validate_service_id( service_id):
    if not check_service_id(service_id):
        return Response(
            data={
                'serviceId': service_id,
                'timestamp': reconvert_to_ms(timezone.now()),
                'errorCode': UzumErrors.InvalidServiceID.value,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return
