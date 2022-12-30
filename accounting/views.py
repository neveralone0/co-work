import random
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Ban, OtpCode
from utils import send_otp_code
from accounting.serializers import UserRegisterSerializer, UserSerializer, BanSerializer
from accounting.permissions import IsAdminOrReadOnly


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        srz_data = UserSerializer(instance=users, many=True)
        return Response(srz_data.data)


class UserLoginAPI(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        phone_number = User.objects.get(phone_number=request.data['phone_number'])
        password = request.data['password']
        if not check_password(password, phone_number.password):
            return Response({'msg': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, phone_number)
        return Response({'message': 'logged in', 'phone': phone_number.phone_number})


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
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class SendOTPCodeAPI(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        check_for_user = User.objects.filter(phone_number=phone_number).exists()
        if not check_for_user:
            return Response({'msg': 'user not found!'})
        # check_for_code = OtpCode.objects.filter(phone_number=phone_number).exists()
        # if check_for_code:
            # return Response({'msg': 'wait 2 minutes!'})
        code = random.randint(1111, 9999)
        send_otp_code(phone_number, code)
        OtpCode.objects.create(phone_number=phone_number, code=code)
        return Response({'msg': 'code sent'})


class VerifyOtpCodeAPI(APIView):
    def post(self, request):
        code = OtpCode.objects.filter(phone_number=request.data['phone_number'])
        if request.data['code'] == code:
            return Response({'msg': 'code is correct'})
        return Response({'msg': 'wrong code!'})


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


class RegisterUser(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        print(request.data)
        # request.POST['national_code'] = int(request.POST['national_code'])
        srz_data = UserRegisterSerializer(data=request.data, partial=True)
        if srz_data.is_valid():
            # print('=1==========')
            # print(srz_data)
            # print('=2==========')
            # print(srz_data.data)
            # print('=3==========')
            # print(srz_data.validated_data)
            # print('lets create')
            # srz_data.validated_data['national_code'] = int(srz_data.validated_data['national_code'])
            srz_data.create(srz_data.validated_data)
            return Response({'msg': 'success'}, status=status.HTTP_201_CREATED)
        print('=e=================')
        print(srz_data.errors)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


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
