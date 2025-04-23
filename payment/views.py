from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from payment.models import PaymeOrder, PaymeTransaction
from payment.serializers import CheckPerformTransactionSerializer, CreateTransactionSerializer, \
    PerformTransactionSerializer, CancelTransactionSerializer, CheckTransactionSerializer
from payment.utils import get_performed_at_datetime, reconvert_to_ms, is_transaction_timed_out


# Create your views here.


class PaymeViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=CheckPerformTransactionSerializer,
        tags=['Payment']
    )
    def post(self, request):
        payme_methods = {
            'CheckPerformTransaction': self.CheckPerformTransaction,
            'CreateTransaction': self.CreateTransaction,
            'PerformTransaction': self.PerformTransaction,
            'CancelTransaction': self.CancelTransaction,
            'CheckTransaction': self.CheckTransaction,
            'GetStatement': None,
            'SetFiscalData': None,

        }
        method = request.data.get('method')
        handler = payme_methods.get(method)
        if handler:
            return handler(request)
        return Response(
            data={
                'error': {
                    'code': -32601,
                    'message': {
                        'uz': 'Metod topilmadi.',
                        'ru': 'Запрашиваемый метод не найден',
                        'en': 'Method not found.'
                    },
                    'data': method
                }
            },
            status=status.HTTP_200_OK
        )

    def CheckPerformTransaction(self, request):
        serializer = CheckPerformTransactionSerializer(data=request.data.get('params'))
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)

        validated_data = serializer.validated_data
        order_id = validated_data['account']['order_id']
        amount = validated_data['amount']

        order = PaymeOrder.objects.filter(order_id=order_id).first()

        if not order:
            return Response(
                data={
                    'error': {
                        'code': -31050,
                        'message': {
                            'uz': 'Buyurtma topilmadi.',
                            'ru': 'Заказ не найден',
                            'en': 'Order not found'
                        },
                        'data': order
                    }
                },
                status=status.HTTP_200_OK
            )
        if order.amount != amount:
            return Response(
                data={
                    'error': {
                        'code': -31001,
                        'message': {
                            'uz': 'Noto\'g\'ri summa.',
                            'ru': 'Неверная сумма.',
                            'en': 'Invalid amount.'
                        },
                        'data': amount
                    }
                },
                status=status.HTTP_200_OK
            )

        return Response(
            data={
                'result': {
                    'allow': True
                }
            },
            status=status.HTTP_200_OK
        )

    def CreateTransaction(self, request):
        serializer = CreateTransactionSerializer(data=request.data.get('params'))
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        transaction_id = validated_data['id']
        performed_at = get_performed_at_datetime(validated_data['time'])
        amount = validated_data['amount']
        order_id = validated_data['account']['order_id']
        account_id = request.user.id
        order = PaymeOrder.objects.filter(order_id=order_id).first()
        if not order:
            return Response(
                data={
                    'error': {
                        'code': -31050,
                        'message': {
                            'uz': 'Buyurtma topilmadi.',
                            'ru': 'Заказ не найден.',
                            'en': 'Order not found.'
                        },
                        'data': order
                    }
                },
                status=status.HTTP_200_OK
            )
        if order.amount != amount:
            return Response(
                data={
                    'error': {
                        'code': -31001,
                        'message': {
                            'uz': 'Noto\'g\'ri summa.',
                            'ru': 'Неверная сумма.',
                            'en': 'Invalid amount'
                        }
                    },
                    'data': order.amount
                },
                status=status.HTTP_200_OK
            )
        transaction = PaymeTransaction.objects.filter(transaction_id=transaction_id).first()
        if transaction:
            if transaction.state != 1:
                return Response(
                    data={
                        'error': {
                            'code': -31008,
                            'message': {
                                'uz': 'Operatsiyani amalga oshirib bo\'lmaydi.',
                                'ru': 'Невозможно выполнить операцию.',
                                'en': 'The operation cannot be completed.'
                            }
                        }
                    },
                    status=status.HTTP_200_OK
                )

            if is_transaction_timed_out(transaction):
                transaction.state = -1
                transaction.save()
                return Response(
                    data={
                        'error': {
                            'code': -31008,
                            'message': {
                                'uz': 'Operatsiyani amalga oshirib bo\'lmaydi.12312313',
                                'ru': 'Невозможно выполнить операцию.',
                                'en': 'The operation cannot be completed.'
                            },
                            'data': transaction
                        }
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                data={
                    'result': {
                        'transaction': transaction_id,
                        'create_time': reconvert_to_ms(transaction.performed_at),
                        'state': transaction.state
                    }
                },
                status=status.HTTP_200_OK
            )

        transaction = PaymeTransaction.objects.create(
            transaction_id=transaction_id,
            performed_at=performed_at,
            amount=amount,
            account_id=account_id,
            state=1,
            payme_order=order,

        )
        return Response(
            data={
                'result': {
                    'create_time': reconvert_to_ms(transaction.performed_at),
                    'transaction': transaction.transaction_id,
                    'state': transaction.state
                }
            },
            status=status.HTTP_200_OK
        )

    def PerformTransaction(self, request):
        serializer = PerformTransactionSerializer(data=request.data.get('params'))
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        print(validated_data)
        transaction_id = validated_data['id']

        transaction = PaymeTransaction.objects.filter(transaction_id=transaction_id).first()

        if not transaction:
            return Response(
                data={
                    'error': {
                        'code': -31003,
                        'message': {
                            'uz': 'Tranzaksiya topilmadi.',
                            'ru': 'Транзакция не найдена.',
                            'en': 'Transaction not found.'
                        },
                        'data': transaction
                    }
                },
                status=status.HTTP_200_OK
            )

        if transaction.state != 1:
            if transaction.state != 2:
                return Response(
                    data={
                        'error': {
                            'code': -31008,
                            'message': {
                                'uz': 'Bu operatsiyani bajarish imkonsiz.',
                                'ru': 'Невозможно выполнить данную операцию.',
                                'en': 'The operation cannoto be completed.'
                            },
                            'data': transaction
                        }
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                data={
                    'result': {
                        'transaction': transaction.transaction_id,
                        'perform_time': reconvert_to_ms(transaction.performed_at),
                        'state': transaction.state
                    }
                },
                status=status.HTTP_200_OK
            )
        if transaction.state == 1:
            if is_transaction_timed_out(transaction):
                transaction.state = -1
                transaction.save()
                return Response(
                    data={
                        'error': {
                            'code': -31008,
                            'message': {
                                'uz': 'Operatsiyani amalga oshirib bo\'lmaydi.12312313',
                                'ru': 'Невозможно выполнить операцию.',
                                'en': 'The operation cannot be completed.'
                            },
                            'data': transaction
                        }
                    },
                    status=status.HTTP_200_OK
                )

        transaction.state = 2
        order = transaction.payme_order
        order.is_paid = 1
        order.save()
        transaction.save()

        return Response(
            data={
                'result': {
                    'transaction': transaction.transaction_id,
                    'perform_time': reconvert_to_ms(transaction.performed_at),
                    'state': 2
                }
            },
            status=status.HTTP_200_OK
        )

    def CancelTransaction(self, request):
        serializer = CancelTransactionSerializer(data=request.data.get('params'))
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        transaction_id = validated_data['id']
        reason = validated_data['reason']

        transaction = PaymeTransaction.objects.filter(transaction_id=transaction_id).first()
        if not transaction:
            return Response(
                data={
                    'error': {
                        'code': -31003,
                        'message': {
                            'uz': 'Tranzaksiya topilmadi.',
                            'ru': 'Транзакция не найдена.',
                            'en': 'Transaction not found.'
                        },
                        'data': transaction
                    }
                },
                status=status.HTTP_200_OK
            )

        if transaction.state == 1:
            transaction.state = -1
            transaction.reason = reason
            transaction.canceled_at = datetime.now()
            transaction.save()
            return Response(
                data={
                    'result': {
                        'transaction': transaction.transaction_id,
                        'cancel_time': reconvert_to_ms(transaction.canceled_at),
                        'state': transaction.state
                    }
                },
                status=status.HTTP_200_OK
            )

        if transaction.state == 2:
            transaction.state = -2
            transaction.reason = reason
            transaction.canceled_at = datetime.now()
            transaction.save()
            return Response(
                data={
                    'result': {
                        'transaction': transaction.transaction_id,
                        'cancel_time': reconvert_to_ms(transaction.canceled_at),
                        'state': transaction.state
                    }
                },
                status=status.HTTP_200_OK
            )

        return Response(
            data={
                'error': {
                    'code': -31008,
                    'message': {
                        'uz': 'Ushbu holatda tranzaksiyani bekor qilib bo‘lmaydi.',
                        'ru': 'Невозможно отменить транзакцию в текущем состоянии.',
                        'en': 'Cannot cancel transaction in current state.'
                    },
                    'state': transaction.state
                }
            },
            status=status.HTTP_200_OK
        )

    def CheckTransaction(self, request):
        serializer = CheckTransactionSerializer(data=request.data.get('params'))
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        transaction_id = validated_data['id']
        transaction = PaymeTransaction.objects.filter(transaction_id=transaction_id).first()

        if not transaction:
            return Response(
                data={
                    'error': {
                        'code': -31003,
                        'message': {
                            'uz': 'Tranzaksiya topilmadi.',
                            'ru': 'Транзакция не найдена.',
                            'en': 'Transaction not found.'
                        },
                        'data': transaction
                    }
                },
                status=status.HTTP_200_OK
            )

        return Response(
            data={
                'result': {
                    'create_time': reconvert_to_ms(transaction.created_at),
                    'perform_time': reconvert_to_ms(transaction.performed_at),
                    'cancel_time': reconvert_to_ms(transaction.canceled_at),
                    'transaction': transaction.transaction_id,
                    'state': transaction.state,
                    'reason': transaction.reason
                }
            },
            status=status.HTTP_200_OK
        )
