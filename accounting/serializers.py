from rest_framework import serializers
from accounting.models import User, Ban


class MiniUserRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, write_only=True)
    uni_code = serializers.IntegerField(required=False)
    working_category = serializers.CharField(required=False)

    def create(self, data):
        data['national_code'] = data['uni_code']
        del(data['uni_code'])
        user_obj = User.objects.create(**data)
        return user_obj


class UserRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, write_only=True)
    full_name = serializers.CharField()
    birth_date = serializers.DateTimeField(required=False)
    picture = serializers.ImageField(required=False)
    uni_code = serializers.IntegerField()
    working_category = serializers.CharField()

    def validate_national_code(self, value):
        # user national code validation here!
        pass

    def create(self, data):
        # these lines used to fix a bug!
        # print('=d==========')
        # print(data)
        data['national_code'] = data['uni_code']
        del(data['uni_code'])
        # print(data)
        # print(validated_data)
        # phone_number, password = validated_data.pop('phone_number'), validated_data.pop('password')
        # user = User.objects.create_user(phone_number=phone_number, password=password)
        user_obj = User.objects.create(**data)

        return user_obj


# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ban
        fields = '__all__'
