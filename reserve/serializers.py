import datetime

import jalali_date
from rest_framework import serializers
from .models import Desk, Reservation
from accounting.models import User
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


class GetReserveSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_name')
    national_code = serializers.SerializerMethodField('get_national_code')
    phone_number = serializers.SerializerMethodField('get_phone_number')

    def get_name(self, instance):
        user = User.objects.get(id=instance.user.id)
        return user.full_name

    def get_national_code(self, instance):
        user = User.objects.get(id=instance.user.id)
        return user.national_code

    def get_phone_number(self, instance):
        user = User.objects.get(id=instance.user.id)
        return user.phone_number

    class Meta:
        model = Reservation
        fields = ('full_name', 'national_code', 'phone_number', 'is_group', 'reservation_time')


class MyReserveSerializer(serializers.ModelSerializer):
    reservation_time = JDateField()
    is_passed = serializers.SerializerMethodField('status')

    def status(self, instance):
        now = datetime.date.today()
        now = jalali_date.date2jalali(now).strftime('%Y-%m-%d')
        now = datetime.datetime.strptime(now, "%Y-%m-%d").date()
        if instance.reservation_time < now:
            return True
        else:
            return False

    class Meta:
        model = Reservation
        fields = ('reservation_time', 'order_time', 'price', 'is_group', 'is_passed')
