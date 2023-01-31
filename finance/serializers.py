from rest_framework import serializers
from .models import Income
from accounting.models import User


class CouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=30)


class IncomeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_name')

    def get_name(self, instance):
        user = User.objects.get(id=instance.user.id)
        return user.full_name

    class Meta:
        model = Income
        fields = ('full_name', 'is_group', 'desk_count', 'order_time', 'price')
