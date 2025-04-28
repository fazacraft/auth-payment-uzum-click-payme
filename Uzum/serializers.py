from rest_framework import serializers


class VerifySerializer(serializers.Serializer):
    serviceId = serializers.IntegerField()
    timestamp = serializers.IntegerField()
    params = serializers.DictField()


class CreateSerializer(serializers.Serializer):
    serviceId = serializers.IntegerField()
    time_stamp = serializers.IntegerField()
    transId = serializers.CharField()
    params = serializers.DictField()
    amount = serializers.IntegerField()


class ConfirmSerializer(serializers.Serializer):
    serviceId = serializers.IntegerField()
    timestamp = serializers.IntegerField()
    transId = serializers.CharField()
    paymentSource = serializers.CharField()
    phone = serializers.CharField()


class CancelSerializer(serializers.Serializer):
    serviceId = serializers.IntegerField()
    timestamp = serializers.IntegerField()
    transId = serializers.CharField()


class CheckStatusSerializer(serializers.Serializer):
    serviceId = serializers.IntegerField()
    timestamp = serializers.IntegerField()
    transId = serializers.CharField()
