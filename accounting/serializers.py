from rest_framework import serializers
from accounting.models import User
from admin_panel.models import Ban


class MiniUserRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, write_only=True)
    
    def create(self, data):
        user_obj = User.objects.create(**data)
        return user_obj


class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, write_only=True)
    full_name = serializers.CharField(required=False)
    birth_date = serializers.DateTimeField(required=False)
    picture = serializers.ImageField(required=False)
    uni_code = serializers.IntegerField(required=False)
    working_category = serializers.CharField(required=False)

    def validate_national_code(self, value):
        # user national code validation here!
        pass

    def create(self, data):
        data['national_code'] = data['uni_code']
        del(data['uni_code'])
        # print(data)
        # print(validated_data)
        # phone_number, password = validated_data.pop('phone_number'), validated_data.pop('password')
        # user = User.objects.create_user(phone_number=phone_number, password=password)
        user_obj = User.objects.create(**data)

        return user_obj

    class Meta:
        model = User
        fields = '__all__'


# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    ban_status = serializers.SerializerMethodField('ban_check')

    def ban_check(self, instance):
        user = User.objects.get(phone_number=instance.phone_number)
        try:
            ban = Ban.objects.get(user=user, status=True)
            return True
        except:
            return False

    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'working_category', 'ban_status', 'national_code')
