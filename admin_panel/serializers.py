from rest_framework import serializers
from .models import Cards, Images, ContactUs, Ban, Quotes
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cards
        fields = '__all__'


# class ImageSerializer(serializers.ModelSerializer):
#     img = serializers.ImageField(max_length=None, use_url=True)
#     class Meta:
#         model = Images
#         fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    # creator = serializers.ReadOnlyField(source='creator.username')
    # creator_id = serializers.ReadOnlyField(source='creator.id')
    img = serializers.ImageField()

    class Meta:
        model = Images
        fields = '__all__'


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class BanSerializer(serializers.ModelSerializer):
    end = JDateField(required=False)
    ending = serializers.IntegerField()

    class Meta:
        model = Ban
        fields = '__all__'


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotes
        fields = '__all__'

