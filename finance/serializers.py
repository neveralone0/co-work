from rest_framework import serializers
from reserve.models import Reservation
from accounting.models import User


class CouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=30)


class ReserveSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_name')

    def get_name(self, instance):
        user = User.objects.get(id=instance.user.id)
        return user.full_name

    class Meta:
        model = Reservation
        fields = ('full_name', 'is_group', 'order_time', 'price')
