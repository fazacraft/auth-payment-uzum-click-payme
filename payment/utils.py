from datetime import datetime
from django.utils import timezone

def get_performed_at_datetime(value):
    return datetime.fromtimestamp(value / 1000)


def reconvert_to_ms(value):
    if not value:
        return 0
    return int(value.timestamp() * 1000)


def is_transaction_timed_out(transaction):
    timeout_ms = 43200000  # 12 hours in ms
    now = timezone.now()
    performed_at = transaction.performed_at

    if timezone.is_naive(performed_at):
        performed_at = timezone.make_aware(performed_at)
    return (now - transaction.performed_at).total_seconds() * 1000 > timeout_ms
