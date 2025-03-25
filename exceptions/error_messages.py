from enum import Enum

from rest_framework import status


class ErrorCodes(Enum):
    UNAUTHORIZED = 1
    INVALID_INPUT = 2
    FORBIDDEN = 3
    NOT_FOUND = 4
    ATTEMPT_ALREADY_EXISTS = 5
    ALREADY_EXISTS = 6
    USER_DOES_NOT_EXIST = 7
    INCORRECT_PASSWORD = 8
    INVALID_TOKEN = 9
    EXPIRED_TOKEN = 10
    VALIDATION_FAILED = 11
    USER_BLOCKED = 12
    DISTRICT_ALREADY_EXISTS = 13
    REGION_ALREADY_EXISTS = 14
    BRANCH_ALREADY_EXISTS = 15
    COST_ALREADY_EXISTS = 16
    EMAIL_ALREADY_EXISTS = 17
    OTP_EXPIRED = 18
    OTP_NO_EXPIRED = 19
    OTP_INVALID = 20
    OTP_ATTEMPT_EXPIRED = 21
    USER_IS_NOT_VERIFIED = 22



error_messages = {
    1: {"result": "Unauthorized access", "http_status": status.HTTP_401_UNAUTHORIZED},
    2: {"result": "Invalid input provided", "http_status": status.HTTP_400_BAD_REQUEST},
    3: {"result": "Permission denied", "http_status": status.HTTP_403_FORBIDDEN},
    4: {"result": "Resource not found", "http_status": status.HTTP_404_NOT_FOUND},
    5: {"result": "You already have 3 attempts, please return after 12 times",
        "http_status": status.HTTP_400_BAD_REQUEST},
    6: {"result": "User Already exists", "http_status": status.HTTP_400_BAD_REQUEST},
    7: {"result": "User Does not exist", "http_status": status.HTTP_400_BAD_REQUEST},
    8: {"result": "Incorrect password", "http_status": status.HTTP_400_BAD_REQUEST},
    9: {"result": "Invalid Token", "http_status": status.HTTP_400_BAD_REQUEST},
    10: {"result": "Token Expired", "http_status": status.HTTP_400_BAD_REQUEST},
    11: {"result": "Validate Error", "http_status": status.HTTP_400_BAD_REQUEST},
    12: {'result': "User blocked", "http_status": status.HTTP_400_BAD_REQUEST},
    13: {'result': "District name already exists", 'http_status': status.HTTP_400_BAD_REQUEST},
    14: {'result': "Region name or ID already exists", 'http_status': status.HTTP_400_BAD_REQUEST},
    15: {'result': "Branch name or ID already exists", 'http_status': status.HTTP_400_BAD_REQUEST},
    16: {'result': "Cost name already exists", 'http_status': status.HTTP_400_BAD_REQUEST},
    17: {'result': "User email already exists", 'http_status': status.HTTP_400_BAD_REQUEST},
    18: {'result': "OTP expired", 'http_status': status.HTTP_400_BAD_REQUEST},
    19: {'result': "OTP has not expired yet", 'http_status': status.HTTP_400_BAD_REQUEST},
    20: {'result': "Invalid OTP code", 'http_status': status.HTTP_400_BAD_REQUEST},
    21: {'result': "The number of attempts has increased, get a new OTP", 'http_status': status.HTTP_400_BAD_REQUEST},
    22: {'result': "User does not verified", 'http_status': status.HTTP_400_BAD_REQUEST}
}


def get_error_message(code):
    return error_messages.get(code, 'Unknown error')
