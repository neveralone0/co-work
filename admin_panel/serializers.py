from rest_framework import serializers
from .models import Cards, Images, ContactUs


class CardSerializer(serializers.ModelSerializer):
    # lis = serializers.ListField(
    #     child=serializers.CharField(max_length=255)
    # )

    # lis = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Cards
        fields = '__all__'


# class LiSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Li
#         fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
