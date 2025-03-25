from django.contrib.auth.hashers import check_password


from authentication.models import User


import requests
from django.conf import settings

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException


def send_notification(message: str) -> None:
    print(4)
    try:
        print(5)
        print(requests.get(settings.TELEGRAM_API_URL + message))
    except Exception as e:
        (print(6))
        print(f"Failed while sending request to telegram client: {e}")


def send_otp(user_id: int, created_at, full_name: str, email: str, otp_code: int, otp_key, type: bool):
    print(2)
    message = (
        f' Project: Olmosbek \nfull name : {full_name}\nuser: {user_id} \nemail: {email}\ncode: {otp_code} '
        f'\notp_key: {otp_key} '
        f'\nReset: {type}'
        f'\ncreated: {created_at}')
    print(3)
    send_notification(message)


def user_login(request):
    data = request.data
    email = data.get('email')
    print(data['password'])

    user = User.objects.filter(email = email).first()
    if not user:
        raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
    if not user.is_verified:
        raise CustomApiException(ErrorCodes.USER_IS_NOT_VERIFIED)

    # if not check_password(data['password'], user.password):
    #     raise CustomApiException(ErrorCodes.INCORRECT_PASSWORD)

    if not check_password(data.get('password'), user.password):
        raise CustomApiException(ErrorCodes.INCORRECT_PASSWORD)

    if not user.status:
        raise CustomApiException(ErrorCodes.USER_BLOCKED)

    return user
