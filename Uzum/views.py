from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from Uzum.const.errors import UzumErrors
from Uzum.const.response_status import UzumResponse
from Uzum.models import UzumbankTransaction
from Uzum.serializers import VerifySerializer, CreateSerializer, ConfirmSerializer, CancelSerializer, \
    CheckStatusSerializer
from Uzum.utils import check_service_id, validate_service_id
from payment.models import PaymeOrder
from payment.utils import reconvert_to_ms


# Create your views here.


class UzumUserViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=VerifySerializer(),
        tags=['Uzum']
    )
    def verify(self, request):
        serializer = VerifySerializer(data=request.data)
        now_ts = reconvert_to_ms(timezone.now())
        if not serializer.is_valid():
            return Response(
                data={
                    'serviceId': request.data.get('serviceId'),
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.MissingRequiredParameters.value,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        service_id_validation = validate_service_id(validated_data['service_id'])
        if service_id_validation: return service_id_validation

        order_id = validated_data['params']['order_id']
        order = PaymeOrder.objects.filter(order_id=order_id).first()

        if not order:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.AdditionalPaymentAttributeNotFound.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if order.is_paid:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.PaymentAlreadyMade.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
                'serviceId': validated_data['service_id'],
                'timestamp': validated_data['time_stamp'],
                'status': UzumResponse.Ok.value,
            },
            status=status.HTTP_200_OK
        )


    @swagger_auto_schema(
        request_body=CreateSerializer,
        tags=['Uzum']
    )
    def create(self, request):
        serializer = CreateSerializer(data=request.data)
        now_ts = reconvert_to_ms(timezone.now())
        if not serializer.is_valid():
            return Response(
                data={
                    'serviceId': request.data.get('serviceId'),
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.MissingRequiredParameters.value,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        service_id_validation = validate_service_id(validated_data['service_id'])
        if service_id_validation: return service_id_validation

        order_id = validated_data['params']['order_id']
        order = PaymeOrder.objects.filter(order_id=order_id).first()
        if not order:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.AdditionalPaymentAttributeNotFound.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if validated_data['amount'] / 100 != order.amount:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.DataVerificationError.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction = UzumbankTransaction.objects.filter(transaction_id=validated_data['trans_id']).first()
        if transaction:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.DataVerificationError.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction = UzumbankTransaction.objects.create(
            transaction_id=validated_data['transaction_id'],
            service_id=validated_data['service_id'],
            time_stamp=now_ts,
            amount=validated_data['amount'] / 100,
            order=order
        )

        return Response(
            data={
                'serviceId': transaction.service_id,
                'transId': transaction.transaction_id,
                'status': transaction.state,
                'transTime': transaction.time_stamp,
                'amount': transaction.amount * 100
            },
            status=status.HTTP_200_OK
        )


    @swagger_auto_schema(
        request_body=ConfirmSerializer,
        tags=['Uzum']
    )
    def confirm(self, request):
        serializer = ConfirmSerializer(data=request.data)
        now_ts = reconvert_to_ms(timezone.now())
        if not serializer.is_valid():
            return Response(
                data={
                    'serviceId': request.data.get('serviceId'),
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.MissingRequiredParameters.value,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        service_id_validation = validate_service_id(validated_data['service_id'])
        if service_id_validation: return service_id_validation

        order_id = validated_data['order_id']
        order = PaymeOrder.objects.filter(order_id=order_id).first()

        if not order:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.AdditionalPaymentAttributeNotFound.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if order.amount != validated_data['amount'] / 100:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.DataVerificationError.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        transaction_id = validated_data['trans_id']
        transaction = UzumbankTransaction.objects.filter(transaction_id=transaction_id).first()

        if not transaction:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.DataVerificationError.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if transaction.state != 1:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.PaymentAlreadyMade.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        transaction.state = 2
        transaction.payment_source = validated_data['payment_source']
        transaction.phone = validated_data['phone']
        transaction.tariff = request.data.get('tariff')
        transaction.processing_reference_number = request.data.get('processingReferenceNumber')
        order.is_paid = True
        transaction.save()
        order.save()

        return Response(
            data={
                'serviceId': transaction.service_id,
                'transId': transaction.transaction_id,
                'status': transaction.state,
                'confirmTime': now_ts,
                'amount': transaction.amount * 100
            }
        )

    @swagger_auto_schema(
        request_body=CancelSerializer,
        tags=['Uzum']
    )
    def cancel(self,request):
        serializer = CancelSerializer(data=request.data)
        now_ts = reconvert_to_ms(timezone.now())
        if not serializer.is_valid():
            return Response(
                data={
                    'serviceId': request.data.get('serviceId'),
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.MissingRequiredParameters.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        service_id_validation = validate_service_id(validated_data['service_id'])
        if service_id_validation: return service_id_validation

        transaction_id = validated_data['transId']
        transaction = UzumbankTransaction.objects.filter(transaction_id = transaction_id).first()

        if not transaction:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.DataVerificationError.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        transaction.state = -1
        transaction.cancelled_at = timezone.now()
        transaction.save()

        return Response(
            data={
                'serviceId': validated_data['service_id'],
                'transId': transaction.transaction_id,
                'status': transaction.state,
                'amount': transaction.amount * 100
            }
        )



    @swagger_auto_schema(
        request_body=CheckStatusSerializer,
        tags=['Uzum']
    )
    def check_status(self,request):
        serializer = CheckStatusSerializer(data=request.data)
        now_ts = reconvert_to_ms(timezone.now())
        if not serializer.is_valid():
            return Response(
                data={
                    'serviceId': request.data.get('serviceId'),
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.MissingRequiredParameters.value,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        service_id_validation = validate_service_id(validated_data['service_id'])
        if service_id_validation: return service_id_validation

        transaction_id = validated_data['trans_id']
        transaction = UzumbankTransaction.objects.filter(transaction_id = transaction_id).first()

        if not transaction:
            return Response(
                data={
                    'serviceId': validated_data['service_id'],
                    'timestamp': now_ts,
                    'errorCode': UzumErrors.DataVerificationError.value
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        return Response(
            data={
                'serviceId': validated_data['service_id'],
                'transId': transaction.transaction_id,
                'status': transaction.state,
                'transTime': transaction.time_stamp
            }
        )



