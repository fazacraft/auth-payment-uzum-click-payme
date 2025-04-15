from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from payment.models import PaymeOrder, Transaction
from payment.serializers import CheckPerformTransactionSerializer, CreateTransactionSerializer
from payment.utils import get_performed_at_datetime, reconvert_to_ms


# Create your views here.


class PaymeViewSet(ViewSet):
   @swagger_auto_schema(
       tags=['Payment   ']
   )
   def post(self, request):
       payme_methods = {
           'CheckPerformTransaction': self.CheckPerformTransaction,
           'CreateTransaction': self.CreateTransaction,
           'PerformTransaction': None,
       }
       method = request.data.get('method')
       handler = payme_methods.get(method)
       if handler:
           return handler(request)
       return Response(
           data={
               'error': 'Invalid Method Braza'
           },
           status = status.HTTP_400_BAD_REQUEST
       )

   def CheckPerformTransaction(self,request):
       serializer = CheckPerformTransactionSerializer(data=request.data.get('params'))
       if not serializer.is_valid():
           raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)

       validated_data = serializer.validated_data
       order_id = validated_data['account']['order_id']
       amount = validated_data['amount']

       order = PaymeOrder.objects.filter(order_id = order_id).first()

       if not order:
           return Response(
               data={
                   'error':{
                       'code': -31050,
                       'message': 'Buyurtma topilmadi',
                       'data': order
                   }
               }
           )
       if order.amount != amount:
           return Response(
               data={
                   'error':{
                       'code':-31001,
                       'message':'Notogri summa',
                       'data': amount
                   }
               }
           )


       return Response(
           data={
               'result':{
                   'allow': True
               }
           }
       )


   def CreateTransaction(self,request):
       serializer = CreateTransactionSerializer(data = request.data.get('params'))
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
                   'error':{
                       'code': -31050,
                       'message': 'Buyurtma topilmadi',
                       'data': order
                   }
               }
           )

       transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
       if transaction:
           return Response(
               data={
                   'result':{
                       'transaction':transaction_id,
                       'create_time': reconvert_to_ms(transaction.performed_at),
                       'state': transaction.state
                   }
               }
           )

       transaction = Transaction.objects.create(
           transaction_id = transaction_id,
           performed_at = performed_at,
           amount = amount,
           account_id = account_id,
           state = 1,
           payme_order = order,

       )
       return Response(
           data={
               'result':{
                   'create_time': transaction.performed_at,
                   'transaction': transaction.transaction_id,
                   'state': transaction.state
               }
           }
       )