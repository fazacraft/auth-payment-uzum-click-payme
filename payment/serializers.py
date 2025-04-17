from rest_framework import serializers




class CheckPerformTransactionSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    account = serializers.DictField()

    def validate_account(self, value):
        if 'order_id' not in value:
            raise serializers.ValidationError('Missing order_id in account')
        return value


class CreateTransactionSerializer(serializers.Serializer):
    id = serializers.CharField()
    time = serializers.IntegerField()
    amount = serializers.FloatField()
    account = serializers.DictField()


class PerformTransactionSerializer(serializers.Serializer):
    id = serializers.CharField()


class CancelTransactionSerializer(serializers.Serializer):
    id = serializers.CharField()
    reason = serializers.IntegerField()


class CheckTransactionSerializer(serializers.Serializer):
    id = serializers.CharField()