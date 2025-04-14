from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from payment.models import PaymeOrder
from payment.serializers import CheckPerformTransactionSerializer


# Create your views here.


class PaymeViewSet(ViewSet):
   @swagger_auto_schema(
       tags=['SomsaXona']
   )
   def post(self, request):
       payme_methods = {
           'CheckPerformTransaction': self.CheckPerformTransaction,
           'CreateTransaction': None,
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

       order = PaymeOrder.objects.filter(id = order_id).first()

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