from rest_framework import serializers

from click.models import ClickTransaction


class PrepareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickTransaction
        fields = [
            'click_trans_id',
            'service_id',
            'click_paydoc_id',
            'merchant_trans_id',
            'amount',
            'action',
            'error',
            'error_note',
            'sign_time',
            'sign_string',
        ]

class CompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickTransaction
        fields = [
            'click_trans_id',
            'service_id',
            'click_paydoc_id',
            'merchant_trans_id',
            'merchant_prepare_id',
            'amount',
            'action',
            'error',
            'error_note',
            'sign_time',
            'sign_string',
        ]
