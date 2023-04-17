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
    working_category = serializers.SerializerMethodField('get_work_category')
    phone_number = serializers.SerializerMethodField('get_phone_number')

    def get_name(self, instance):
        user = User.objects.get(id=instance.user.id)
        return user.full_name

    def get_work_category(self, instance):
        user = User.objects.get(id=instance.user.id)
        return user.working_category

    def get_phone_number(self, instance):
        user = User.objects.get(id=instance.user.id)
        return user.phone_number

    class Meta:
        model = Reservation
        fields = ('id', 'full_name', 'working_category', 'phone_number',
                  'is_group', 'reservation_time', 'order_time', 'price')


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


class UserVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=13)
    otp = serializers.CharField(required=False)

    def mobile_validation(self, phone):
        if not str(phone)[1:].isnumeric():
            raise serializers.ValidationError("please enter a Valid Number")
        elif not str(phone).startswith("09") or str(phone).startswith("+989"):
            raise serializers.ValidationError("please enter a Valid Number")
        elif len(phone) != 11 or 13:
            raise serializers.ValidationError("please enter a Valid Number")
        return phone

    def otp_validation(self, otp):
        if len(otp) != 6:
            raise serializers.ValidationError("Please enter a correct code")
        elif not str(otp).isnumeric():
            raise serializers.ValidationError("Please enter a correct code")
        return otp


class UserLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=13)

    def mobile_validation(self, phone):
        if not str(phone)[1:].isnumeric():
            raise serializers.ValidationError("please enter a Valid Number")
        elif not str(phone).startswith("09") or str(phone).startswith("+98"):
            raise serializers.ValidationError("please enter a Valid Number")
        elif len(phone) != 11 or 13:
            raise serializers.ValidationError("please enter a Valid Number")
        return phone