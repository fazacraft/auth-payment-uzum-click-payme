from enum import Enum


class UzumErrors(Enum):
    AccessDenied = 10001
    JSONParsingError = 10002
    InvalidOperation = 10003
    MissingRequiredParameters = 10005
    InvalidServiceID = 10006
    AdditionalPaymentAttributeNotFound = 10007
    PaymentAlreadyMade = 10008
    PaymentCancelled = 10009
    DataVerificationError = 99999

