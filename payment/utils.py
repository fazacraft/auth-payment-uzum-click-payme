from datetime import datetime
import time

def get_performed_at_datetime(value):
    return datetime.fromtimestamp(value.performed_at / 1000)



def reconvert_to_ms(value):
    return int(value.timestamp() * 1000)