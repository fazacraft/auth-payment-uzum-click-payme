from datetime import timedelta, timezone, datetime

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User, OTP
from authentication.serializers import UserSerializer, OTPSerializer, LoginSerializer
from authentication.utils import send_otp, user_login
from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException


# Create your views here.


class UserViewSet(ModelViewSet):

    @swagger_auto_schema(
        operation_description='Create a new user!',
        operation_summary='You can create a new user here!',
        request_body=UserSerializer,
        responses={
            201: openapi.Response(description="OK", schema=UserSerializer)
        },
        tags=['User']
    )
    def create(self, request):

        data = request.data
        print(data)
        user = User.objects.filter(email=data.get('email')).first()
        print(user)
        if user and user.is_verified:
            raise CustomApiException(ErrorCodes.ALREADY_EXISTS, message='User already exists!')
        if user:
            serializer = UserSerializer(user, data=data, context={'request': request}, partial=True)
        else:
            serializer = UserSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message=serializer.errors)
        user = serializer.save()
        otp = OTP.objects.create(user=user)
        otp.save()


        send_otp(user_id=otp.user_id, created_at=otp.created_at,full_name=otp.user.full_name, otp_code=otp.otp_code, otp_key=otp.otp_key,
                 type=otp.reset, email=otp.user.email)

        return Response(
            data={
                'result': {'otp_key': otp.otp_key},
                'details': serializer.data,
                'ok': True
            },
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_summary='Update Customer api',
        operation_description='Update Customer api',
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "full_name": openapi.Schema(type=openapi.TYPE_STRING, description="Updated full name"),
                        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Updated password (hashed)"),
                    }
                )
            )
        },
        tags=['User']
    )
    def update(self, request, pk):
        data = request.data
        user = User.objects.filter(id=pk).first()
        if not user:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
        serializer = UserSerializer(user, data=data, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, serializer.errors)
        serializer.save()

        return Response(
            data={
                'result': {
                        'full_name': serializer.validated_data['full_name'],
                        'password': serializer.validated_data['password'],
                },
                'ok': True
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description='Get details!',
        responses={
            200: openapi.Response(description="OK", schema=UserSerializer)
        },
        tags=['User']
    )
    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
        return Response(
            data={
                'result': UserSerializer(user).data,
                'ok': True
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='OK')
        },
        tags=['User']
    )
    def delete(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
        user.delete()
        return Response(
            data={
                'result': 'Successfully Deleted!',
                'ok': True
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description='Verify user!',
        operation_summary='You can verify ur self',
        request_body=OTPSerializer,
        responses={
            201: openapi.Response(description='OK', schema=OTPSerializer)
        },
        tags=['User OTP']
    )
    def otp_verify(self, request):
        serializer = OTPSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED)

        otp = OTP.objects.filter(otp_key=serializer.validated_data.get('otp_key')).first()
        if not otp:
            raise CustomApiException(ErrorCodes.NOT_FOUND)

        otp.attempt += 1
        otp.save()

        if timezone.now() - otp.created_at > timedelta(minutes=2):
            raise CustomApiException(ErrorCodes.OTP_EXPIRED)
        if otp.attempt > 3:
            raise CustomApiException(ErrorCodes.OTP_ATTEMPT_EXPIRED)
        if otp.otp_code != serializer.validated_data.get('otp_code'):
            raise CustomApiException(ErrorCodes.OPT_INVALID)
        otp.user.is_verified = True
        otp.user.save()
        otp.user.otp_user.all().delete()

        return Response(
            data={
                'result': 'User verified succesfully!',
                'ok': True,
            },
            status=status.HTTP_200_OK
        )
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type= openapi.TYPE_OBJECT,
            required=['otp_key'],
            properties={
                "otp_key": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_UUID,
                    description="Unique OTP key for verification"
                )}),
        responses={
            200: openapi.Response(description='OK', schema=OTPSerializer)
        },
            tags=['User OTP']
        )
    def otp_resend(self, request):
        otp_key = request.data.get('otp_key')
        if not otp_key:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED)
        otp = OTP.objects.filter(otp_key = otp_key).first()
        if not otp:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED)
        if timezone.now() - otp.created_at < timedelta(minutes=2):
            raise CustomApiException(ErrorCodes.OTP_NO_EXPIRED)
        if otp_key != str(otp.user.otp_user.all().first().otp_key):
            raise CustomApiException(ErrorCodes.OTP_INVALID)
        new_otp = OTP.objects.create(user=otp.user)
        new_otp.save()
        send_otp(user_id=new_otp.user_id, created_at=new_otp.created_at, full_name=new_otp.user.full_name, otp_code=new_otp.otp_code,
                 otp_key=new_otp.otp_key,
                 type=new_otp.reset, email=new_otp.user.email)

        return Response(data={'result': {"otp_key": new_otp.otp_key}, 'ok': True}, status=status.HTTP_200_OK)


class UserLoginViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='User Login!',
        operation_description='User login via email and password!',
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description="OK")
        },
        tags=['User Login']
    )
    def login(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)

        user = user_login(request)
        login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user.login_time = login_time
        user.save()

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['role'] = user.role
        access_token['login_time'] = login_time

        return Response(
            data = {
                'result':{
                    'access_token': str(access_token),
                    'refesh_token': str(refresh_token),
                },
                'ok': True
            },
            status=status.HTTP_200_OK
        )
