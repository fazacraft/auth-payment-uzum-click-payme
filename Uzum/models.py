from django.db import models

from abstract_model.base_model import BaseModel
from payment.models import STATE_CHOICES, PaymeOrder


# Create your models here.
STATUS_CHOICE = (
    (1, 'CREATED'),
    (2, 'CONFIRMED'),
    (-1, 'CANCELLED'),
)

class UzumbankTransaction(BaseModel):
    transaction_id = models.CharField()
    service_id = models.BigIntegerField()
    time_stamp = models.BigIntegerField()
    amount = models.BigIntegerField()
    tariff = models.CharField(blank=True, null=True)
    payment_source = models.CharField(blank=True, null=True)
    processing_reference_number = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    reverse_time= models.DateTimeField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(choices=STATUS_CHOICE, default=1)
    order = models.ForeignKey(PaymeOrder,on_delete=models.CASCADE, related_name='uzumbank_order')


    def __str__(self):
        return self.transaction_id


