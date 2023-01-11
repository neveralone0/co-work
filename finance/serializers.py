from rest_framework import serializers


class CouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=30)