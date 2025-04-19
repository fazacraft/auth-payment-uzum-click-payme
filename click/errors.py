from enum import Enum


class ClickErrorCodes(Enum):
    Success = 0
    SignedFailed = -1
    InvalidAmount = -2
    ActionNotFound = -3
    AlreadyPaid = -4
    UserNotFound = -5
    TransactionNotFound = -6
    FailedToUpdateUser = -7
    ErrorInRequestFromClick = -8
    TransactionCancelled = -9





