from rest_framework import serializers


class SignInSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    passcode = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        return data
