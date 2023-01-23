from rest_framework import serializers
from .models import Desk, Reservation
from django_jalali.serializers.serializerfield import JDateField


class FreeDeskSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class DeskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Desk
        fields = '__all__'


class ReserveSerializer(serializers.ModelSerializer):
    reservation_time = serializers.DateField()

    class Meta:
        model = Reservation
        fields = '__all__'


class MyReserveSerializer(serializers.ModelSerializer):
    reservation_time = JDateField()

    class Meta:
        model = Reservation
        fields = ('reservation_time', 'order_time', 'price', 'is_group')
    # reservation_time = serializers.DateField()
    # order_time = serializers.DateField()
    # price = serializers.IntegerField()
    # is_group = serializers.BooleanField()
