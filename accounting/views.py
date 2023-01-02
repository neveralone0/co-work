import random

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User, Ban, OtpCode
from utils import send_otp_code
from accounting.serializers import UserRegisterSerializer, UserSerializer, BanSerializer, MiniUserRegisterSerializer
from accounting.permissions import IsAdminOrReadOnly, IsNotBanned
from helpers.helpers import WORKING_CATEGORY


class RegisterUser(APIView):
    serializer_class = MiniUserRegisterSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data, partial=True)
        if srz_data.is_valid():
            phone_number = srz_data.validated_data['phone_number']
            if not phone_number.isdigit():
                return Response({'msg': 'phone number must be all num!'})
            if self.check_for_user(phone_number):
                return Response({'msg': 'user exists, use otp code and login!'}, status=status.HTTP_400_BAD_REQUEST)
            if SendOTPCodeAPI.check_for_existing_code(self, phone_number):
                return Response({'msg': 'wait 2 minutes'}, status=status.HTTP_400_BAD_REQUEST)
            create = False
            try:
                check_for_user = User.objects.get(phone_number=phone_number)
                if check_for_user.phone_number_validation:
                    return Response({'msg': 'user exists, use otp code and login!'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    check_for_user.delete()
                    create = True
            except:
                srz_data.create(srz_data.validated_data)
            if create:
                srz_data.create(srz_data.validated_data)
            SendOTPCodeAPI.create_otp_code(self, phone_number=phone_number)
            return Response({'msg': 'otp sent'}, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_for_user(self, phone_number):
        try:
            check_for_user = User.objects.get(phone_number=phone_number)
            if check_for_user.phone_number_validation:
                return True
            return False
        except:
            return False


class SendOTPCodeAPI(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        # if not RegisterUser.check_for_user(phone_number):
        #     return Response({'msg': 'user does not exists please register'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            check_for_user = User.objects.get(phone_number=phone_number)
            if not check_for_user:
                return Response({'msg': 'register first!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        if self.check_for_existing_code(phone_number):
            return Response({'msg': 'wait 2 minutes'}, status=status.HTTP_400_BAD_REQUEST)
        self.create_otp_code(phone_number)
        return Response({'msg': 'code sent'})

    def check_for_existing_code(self, phone_number):
        check_for_code = OtpCode.objects.filter(phone_number=phone_number).exists()
        if check_for_code:
            return True
        return False

    def create_otp_code(self, phone_number):
        code = random.randint(1111, 9999)
        print('=otp============')
        print(code)
        # send_otp_code(phone_number, code)
        if not phone_number.isdigit():
            return Response({'msg': 'phone number must be all num!'})

        OtpCode.objects.create(phone_number=phone_number, code=code)
        return Response({'msg': 'code sent'})


class VerifyOtpCodeAPI(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        code = request.data['code']
        try:
            check_for_user = User.objects.get(phone_number=phone_number)
            if not check_for_user:
                return Response({'msg': 'register first!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        try:
            code_var = OtpCode.objects.get(phone_number=phone_number, code=code)
        except:
            return Response({'msg': 'code is wrong or expired!'}, status=status.HTTP_400_BAD_REQUEST)
        if code_var.code == int(code):
            self.verify_user(request)
            user = User.objects.get(phone_number=phone_number)
            refresh = RefreshToken.for_user(user)
            try:
                code_var.delete()
            except: pass
            return Response({'msg': 'verified, logged in successfully',
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)})

    def verify_user(self, request):
        user = User.objects.get(phone_number=request.data['phone_number'])
        if not user.phone_number_validation:
            user.phone_number_validation = True
            user.save()
        return Response({})

    # def login_via_password(self, request):
    #     phone_number = User.objects.get(phone_number=request.data['phone_number'])
    #     password = request.data['password']
    #     if not check_password(password, phone_number.password):
    #         return Response({'msg': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    #     login(request, phone_number)
    #     return Response({'message': 'logged in', 'phone': phone_number.phone_number})


class UpdateUserInfo(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsNotBanned]

    def post(self, request):
        user = request.user.phone_number
        user = User.objects.get(phone_number=user)
        srz_data = self.serializer_class(data=request.data, instance=user, partial=True)
        if srz_data.is_valid():
            return Response({'message': 'updated'})


class GetWorkingCategory(APIView):
    def get(self, request):
        items = list()
        for item in WORKING_CATEGORY:
            print()
            items.append(item[1])

        return Response({'topic': items, 'is_ok': True})


class GetUserViaPhoneAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request):
        try:
            phone = request.data['phone_number']
        except:
            return Response({'msg': 'phone number is empty'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(phone_number=phone)
        srz_data = UserSerializer(instance=user)
        return Response(srz_data.data)


class GetUsersListAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        srz_data = UserSerializer(instance=users, many=True)
        return Response(srz_data.data)


class ResetPasswordAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        password = request.data['password']
        if not check_password(password, request.user.password):
            print('wrong!')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['new_password'])
        user.save()
        return Response({'message': 'ok'})


class RemoveUserAPI(APIView):
    permission_classes = [IsAdminUser, IsAdminUser]

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return Response({'message': 'user deleted successfully'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BanUserAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BanSerializer

    def post(self, request):
        srz_data = BanSerializer(data=request.data)
        if srz_data.is_valid():
            user = request.user.id
            user = get_object_or_404(User, pk=user)
            user = user.banns.objects.filter(status=True).exists()
            if user:
                return Response({'msg': 'user already banned!'}, status=status.HTTP_400_BAD_REQUEST)
            srz_data.save()
            return Response({'msg': 'user banned'})


class UnbanUserAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        ban_objects = Ban.objects.filter(user=request.user.id, status=True)
        for obj in ban_objects:
            obj.status = False
            obj.save()
        return Response({'msg': 'user unbanned!'})


class CurrentlyBannedUsersAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BanSerializer

    def post(self, request):
        banned_users = Ban.objects.filter(status=True)
        srz_data = BanSerializer(instance=banned_users, many=True)
        return Response(srz_data.data)


class CurrentUserBanHistoryAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BanSerializer

    def get(self, request):
        ban_history = Ban.objects.filter(user=request.user.id)
        srz_data = BanSerializer(instance=ban_history, many=True)
        return Response(srz_data.data)


class CurrentUserBanStatusAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BanSerializer

    def get(self, request):
        ban_status = Ban.objects.filter(user=request.user.id, status=True).exists()
        srz_data = BanSerializer(instance=ban_status)
        return Response(srz_data.data)


class RemoveAllCodes(APIView):
    def post(self, request):
        codes = OtpCode.objects.all()
        codes.delete()
        return Response({'msg': 'deleted'})
