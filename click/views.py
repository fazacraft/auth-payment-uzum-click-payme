from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from click.errors import ClickErrorCodes
from click.models import ClickTransaction
from click.serializers import PrepareSerializer, CompleteSerializer
from click.utils import check_sign_string_prepare, check_sign_string_complete
from payment.models import PaymeOrder



# Create your views here.


class ClickViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=PrepareSerializer,
        tags=['Click']
    )
    def prepare(self, request):
        serializer = PrepareSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'error': ClickErrorCodes.ErrorInRequestFromClick.value,
                    'error_note': ClickErrorCodes.ErrorInRequestFromClick.name
                },
                status=status.HTTP_200_OK
            )
        validated_data = serializer.validated_data
        flag = check_sign_string_prepare(
            validated_data['click_trans_id'],
            validated_data['merchant_trans_id'],
            validated_data['amount'],
            validated_data['action'],
            validated_data['sign_time'],
            validated_data['sign_string']
        )
        if not flag:
            return Response(
                data={
                    'error': ClickErrorCodes.SignedFailed.value,
                    'error_note': ClickErrorCodes.SignedFailed.name
                },
                status=status.HTTP_200_OK
            )
        order = PaymeOrder.objects.filter(order_id=validated_data['merchant_trans_id']).first()

        if not order:
            return Response(
                data={
                    'error': ClickErrorCodes.UserNotFound_Or_OrderNotFound.value,
                    'error_note': ClickErrorCodes.UserNotFound_Or_OrderNotFound.name
                },
                status=status.HTTP_200_OK
            )
        if order.amount != validated_data['amount']:
            return Response(
                data={
                    'error': ClickErrorCodes.InvalidAmount.value,
                    'error_note': ClickErrorCodes.InvalidAmount.name
                },
                status=status.HTTP_200_OK
            )
        if order.is_paid == 1:
            return Response(
                data={
                    'error': ClickErrorCodes.AlreadyPaid.value,
                    'error_note': ClickErrorCodes.AlreadyPaid.name
                },
                status=status.HTTP_200_OK
            )
        if validated_data['action'] < 0:
            return Response(
                data={
                    'error': ClickErrorCodes.ErrorInRequestFromClick.value,
                    'error_note': ClickErrorCodes.ErrorInRequestFromClick.name,
                    'click_trans_id': validated_data.click_trans_id,
                    'merchant_trans_id': order.order_id,

                }
            )


        transaction = ClickTransaction.objects.create(
            click_trans_id = validated_data['click_trans_id'],
            service_id = validated_data['service_id'],
            click_paydoc_id = validated_data['click_paydoc_id'],
            merchant_trans_id = validated_data['merchant_trans_id'],
            amount = validated_data['amount'],
            action = validated_data['action'],
            error = validated_data['error'],
            error_note = validated_data['error_note'],
            sign_time = validated_data['sign_time'],
            sign_string = validated_data['sign_string'],
            order = order
        )
        transaction.merchant_prepare_id = transaction.id
        transaction.save()
        return Response(
            data={
                'error': ClickErrorCodes.Success.value,
                'error_note': ClickErrorCodes.Success.name,
                'click_trans_id': transaction.click_trans_id,
                'merchant_trans_id': transaction.order.order_id,
                'merchant_prepare_id': transaction.merchant_prepare_id
            },
            status=status.HTTP_200_OK
        )


    @swagger_auto_schema(
        request_body=CompleteSerializer,
        tags=['Click']
    )
    def complete(self,request):
        serializer = CompleteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'error': ClickErrorCodes.ErrorInRequestFromClick.value,
                    'error_note': ClickErrorCodes.ErrorInRequestFromClick.name
                },
                status=status.HTTP_200_OK
            )

        validated_data = serializer.validated_data
        flag = check_sign_string_complete(
            validated_data['click_trans_id'],
            validated_data['merchant_trans_id'],
            validated_data['merchant_prepare_id'],
            validated_data['amount'],
            validated_data['action'],
            validated_data['sign_time'],
            validated_data['sign_string']
        )
        if not flag:
            return Response(
                data={
                    'error': ClickErrorCodes.SignedFailed.value,
                    'error_note': ClickErrorCodes.SignedFailed.name
                },
                status=status.HTTP_200_OK
            )



        transaction = ClickTransaction.objects.filter(
            merchant_prepare_id = validated_data['merchant_prepare_id']
        ).first()

        if not transaction or transaction.click_trans_id != validated_data['click_trans_id']:
            return Response(
                data={
                    'error': ClickErrorCodes.TransactionNotFound.value,
                    'error_note': ClickErrorCodes.TransactionNotFound.name,
                },
                status=status.HTTP_200_OK
            )


        order = PaymeOrder.objects.filter(order_id = validated_data['merchant_trans_id']).first()
        if not order:
            return Response(
                data={
                    'error':ClickErrorCodes.UserNotFound_Or_OrderNotFound.value,
                    'error_note': ClickErrorCodes.UserNotFound_Or_OrderNotFound.name
                },
                status=status.HTTP_200_OK
            )
        if order.is_paid == 1:
            return Response(
                data={
                    'error': ClickErrorCodes.AlreadyPaid.value,
                    'error_note': ClickErrorCodes.AlreadyPaid.name
                },
                status=status.HTTP_200_OK
            )
        if order.amount != validated_data['amount']:
            return Response(
                data={
                    'error': ClickErrorCodes.InvalidAmount.value,
                    'error_note': ClickErrorCodes.InvalidAmount.name
                },
                status=status.HTTP_200_OK
            )
        if validated_data['error'] < 0:
            return Response(
                data={
                    'error': ClickErrorCodes.TransactionCancelled.value,
                    'error_note': ClickErrorCodes.TransactionCancelled.name
                }
            )
        order.is_paid = True
        order.save()
        transaction.state = 2
        return Response(
            data={
                'error': ClickErrorCodes.Success.value,
                'error_note': ClickErrorCodes.Success.name,
                'click_trans_id': transaction.click_trans_id,
                'merchant_trans_id': transaction.order.order_id
            },
            status=status.HTTP_200_OK
        )