from rest_framework import serializers


class VerifySerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    time_stamp = serializers.IntegerField()
    params = serializers.DictField()


class CreateSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    time_stamp = serializers.IntegerField()
    trans_id = serializers.CharField()
    params = serializers.DictField()
    amount = serializers.IntegerField()


class ConfirmSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    time_stamp = serializers.IntegerField()
    trans_id = serializers.CharField()
    payment_source = serializers.CharField()
    phone = serializers.CharField()


class CancelSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    time_stamp = serializers.IntegerField()
    trans_id = serializers.CharField()


class CheckStatusSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    time_stamp = serializers.IntegerField()
    trans_id = serializers.CharField()
