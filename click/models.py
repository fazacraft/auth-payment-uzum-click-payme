from django.db import models

from abstract_model.base_model import BaseModel
from payment.models import PaymeOrder, STATE_CHOICES


# Create your models here.



class ClickTransaction(BaseModel):
    click_trans_id = models.BigIntegerField()
    service_id = models.IntegerField()
    click_paydoc_id = models.BigIntegerField()
    merchant_trans_id = models.CharField()
    amount = models.FloatField()
    action = models.SmallIntegerField()
    error = models.IntegerField()
    error_note = models.CharField()
    sign_time = models.CharField()
    sign_string = models.CharField()
    merchant_prepare_id = models.IntegerField(blank=True, null=True)
    merchant_confirm_id = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey(PaymeOrder, on_delete=models.CASCADE, related_name='payme_order_click')
    state = models.IntegerField(choices=STATE_CHOICES, default=1)

    def __str__(self):
        return self.merchant_trans_id