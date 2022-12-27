from rest_framework import serializers

from accounting.models import User, Ban


class UserRegisterSerializer(serializers.Serializer):
    # national_code = serializers.IntegerField()
    phone_number = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    # user_code = serializers.CharField()
    birth_date = serializers.DateTimeField(required=False)
    picture = serializers.ImageField(required=False)
    uni_code = serializers.IntegerField()

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
