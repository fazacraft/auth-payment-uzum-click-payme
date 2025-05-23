from tkinter.constants import CASCADE

from django.db import models
from authentication.models import User
from abstract_model.base_model import BaseModel


# Create your models here.
STATE_CHOICES = (
    (0, 'initial'),
    (1, 'created'),
    (2, 'paid'),
    (-1, 'cancelled'),
)

STATUS_CHOICES = (
    (0,'pending'),
    (1,'paid'),
    (-1, 'cancelled')
)
class PaymeOrder(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payme_user')
    order_id = models.CharField(max_length=255, unique=True)
    amount = models.FloatField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Payme Order {self.order_id}'

class PaymeTransaction(BaseModel):
    transaction_id = models.CharField(max_length=255, unique=True)
    account_id = models.CharField(max_length=255, blank=True, null = True)
    payme_order = models.ForeignKey(PaymeOrder, on_delete=models.CASCADE, related_name='payme_order')
    amount = models.FloatField()
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=0)
    performed_at = models.DateTimeField(blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    reason = models.SmallIntegerField(blank=True, null=True)


    def __str__(self):
        return f'user_id {self.account_id}: Transaction_id {self.transaction_id} for payme_order {self.payme_order}'
