from rest_framework import serializers
from .models import Desk, Reservation


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = '__all__'


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
