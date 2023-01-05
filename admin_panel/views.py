from rest_framework.decorators import action
from rest_framework.views import APIView, Response, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from reserve.models import Reservation, Desk
from reserve.serializers import ReserveSerializer, DeskSerializer
from .serializers import *
from .models import *


class GetAllImage(APIView):
    serializer_class = ImageSerializer

    def get(self, request):
        images = Images.objects.all()
        srz_data = self.serializer_class(instance=images, many=True)
        return Response(srz_data.data)


class UploadImage(APIView):
    serializer_class = ImageSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response({'msg': 'image uploaded'}, status=status.HTTP_201_CREATED)
        return Response({srz_data.errors})


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Images.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        serializer.save()
    #
    # def createe(self, request):
    #     serializer = ImageSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'msg': 'ok'})
    #


class DeleteImage(APIView):
    def delete(self, request):
        id = request.data['id']
        img = Images.objects.filter(id=id)
        img.delete()
        return Response({'msg': 'deleted'})


class ListDeleteImages(APIView):
    def delete(self, request):
        ids = request.data['ids']
        imgs = Images.objects.filter(id__in=ids)
        for img in imgs:
            img.delete()
        return Response({'msg': 'deleted'})


class ContactUsGet(APIView):
    serializer_class = ContactUsSerializer

    def get(self, request):
        info = ContactUs.objects.get(pk=1)
        srz_data = self.serializer_class(instance=info)
        return Response(srz_data.data)


class ContactUsUpdate(APIView):
    def post(self, request):
        info = ContactUs.objects.get(pk=1)
        srz_data = self.serializer_class(data=request.data, instance=info)
        if srz_data.is_valid():
            srz_data.save()
            return Response({'msg': 'information updated'})


class CardAPI(APIView):
    serializer_class = CardSerializer

    def get(self, request):
        cards = Cards.objects.all()
        srz_data = self.serializer_class(instance=cards, many=True)
        return Response(srz_data.data)

    def post(self, request):
        for card in request.data:
            obj = Cards.objects.get(id=card['id'])
            srz_data = self.serializer_class(data=card, instance=obj)
            if srz_data.is_valid():
                srz_data.save()
            return Response({'msg': 'cards updated'})


# class AddLi(APIView):
#     serializer_class = LiSerializer
#
#     def post(self, request):
#         srz_data = self.serializer_class(data=request.data)
#         if srz_data.is_valid():
#             srz_data.save()
#             return Response({'msg': 'li added'})

#
# class UpdateLi(APIView):
#     serializer_class = LiSerializer
#
#     def put(self, request, pk):
#         lis = Li.objects.get(pk=pk)
#         srz_data = self.serializer_class(instance=lis, data=request.data, many=True)
#         if srz_data.is_valid():
#             srz_data.save()
#             return Response({'msg': 'li updated'})
#
#
# class DeleteLi(APIView):
#     def delete(self, request, pk):
#         li = Li.objects.get(pk=pk)
#         li.delete()
#         return Response({'msg': 'li deleted'})


class MyModelViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        print('saved')
        serializer.save()


class BanUserAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BanSerializer

    def post(self, request):
        srz_data = BanSerializer(data=request.data)
        print('-1')
        if srz_data.is_valid():
            user = request.data['user']
            print('0')
            try:
                print('1')
                check = User.objects.filter(bans__status=True, id=user).exists()
                if check:
                    print('okk')
                    return Response({'msg': 'user already banned!'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({'msg': 'user not found!'}, status=status.HTTP_400_BAD_REQUEST)
            print('3')
            srz_data.create(validated_data=srz_data.validated_data)
            print('6')
            return Response({'msg': 'user banned'})
        print('============')
        print(srz_data.errors)


class UnbanUserAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        user = request.data['user']
        ban_objects = Ban.objects.filter(user=user, status=True)
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


class UserBanHistoryAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BanSerializer

    def get(self, request):
        user = request.data['user']
        ban_history = Ban.objects.filter(user=user)
        srz_data = BanSerializer(instance=ban_history, many=True)
        return Response(srz_data.data)


class UserBanStatusAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BanSerializer

    def get(self, request):
        user = request.data['user']
        ban_status = Ban.objects.filter(user=user, status=True).exists()
        if ban_status:
            return Response({'mas': 'user is banned'})
        return Response({'mas': 'user is not banned'})


class CreateDeskAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = DeskSerializer

    def post(self, request):
        srz_data = DeskSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response({'msg': 'created'})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteDeskAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        desk = Desk.objects.filter(pk=pk)
        desk[0].delete()
        return Response({'msg': 'deleted'})


class DeskListDeleteAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request):
        desk_ids = request.data['desks']
        desks = Desk.objects.filter(id__in=desk_ids)
        for desk in desks:
            desk.delete()
        return Response({'msg': 'desks deleted'})


class GetAllReservesAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReserveSerializer

    def get(self, request):
        reserves = Reservation.objects.all()
        srz_data = ReserveSerializer(instance=reserves, many=True)
        return Response(srz_data.data)


class ChangeDeskPriceAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        desk_obj = get_object_or_404(Desk, id=request.data['desk_id'])
        desk_obj.price = request.data['price']
        desk_obj.save()



class GetThisWeekReservesAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        pass



class ChangeMultiDesksPriceAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        desk_list = Desk.objects.filter(id__in=request.data['desk_list'])
        price = request.data['price']
        for desk in desk_list:
            desk.price = price
            desk.save()


class ChangeAllDesksPriceAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        desk_list = Desk.objects.all()
        price = request.data['price']
        for desk in desk_list:
            desk.price = price
            desk.save()


class AdminReserveDeskAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReserveSerializer

    def post(self, request):
        srz_data = ReserveSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AdminCancelReservationAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        reserve_id = request.data['reserve_id']
        reserve_obj = Reservation.objects.filter(id=reserve_id).exists()
        reserve_obj.delete()
        return Response({'msg': 'object deleted'})

