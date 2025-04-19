from hashlib import md5

from config import settings


def encrypt(test_string):
    hashed = md5(test_string.encode()).hexdigest()
    return hashed


def check_sign_string(click_trans_id, merchant_trans_id, amount, action, sign_time, sign_string):
    test_string = (
            str(click_trans_id)
            + str(settings.CLICK_SERVICE_ID)
            + settings.CLICK_SECRET_KEY
            + str(merchant_trans_id)
            + str(amount)
            + str(action)
            + str(sign_time)
    )
    hashed_test_string = encrypt(test_string)
    return hashed_test_string == sign_string