from rest_framework import serializers

from common.models import Order


class SignInSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    passcode = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'class_index', 'customer_first_name', 'customer_last_name',
            'customer_middle_name', 'phone_number', 'albums_count',
            'passcode', 'status', 'studio', 'school'
        )
        read_only_fields = (
            'id', 'class_index', 'customer_first_name', 'customer_last_name',
            'customer_middle_name', 'phone_number', 'albums_count',
            'passcode', 'status', 'studio', 'school'
        )
