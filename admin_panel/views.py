import datetime
import jalali_date
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.views import APIView, Response, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from accounting.serializers import UserSerializer
from reserve.views import ReserveDeskAPI
from reserve.models import Reservation, Desk
from reserve.serializers import ReserveSerializer, DeskSerializer
from .serializers import *
from utils import UserFilter
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
        # srz_data = BanSerializer(instance=banned_users, many=True)
        payload = Paginate.page(self, request, banned_users, self.serializer_class)
        return Response(payload)


class UserBanHistoryAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BanSerializer

    def get(self, request):
        user = request.data['user']
        ban_history = Ban.objects.filter(user=user)
        # srz_data = BanSerializer(instance=ban_history, many=True)
        payload = Paginate.page(self, request, ban_history, self.serializer_class)
        return Response(payload)


class UserBanStatusAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BanSerializer

    def get(self, request):
        user = request.data['user']
        ban_status = Ban.objects.filter(user=user, status=True).exists()
        if ban_status:
            return Response({'mas': 'user is banned'})
        return Response({'mas': 'user is not banned'})


class BanHistoryAPI(APIView):
    serializer_class = Ban

    def post(self, request):
        ban = Ban.objects.all()
        payload = Paginate.page(self, request, ban, self.serializer_class)
        return Response(payload)



class GetDesks(APIView):
    # permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = DeskSerializer

    def get(self, request):
        desk_list = Desk.objects.all()
        srz_data = DeskSerializer(instance=desk_list, many=True)
        return Response(srz_data.data)


class GetSpecificDeskAPI(APIView):
    serializer_class = DeskSerializer

    def get(self, desk_id):
        desk = Desk.objects.get(pk=desk_id)
        srz_data = DeskSerializer(instance=desk)
        return Response(srz_data.data)


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
        # srz_data = ReserveSerializer(instance=reserves, many=True)
        payload = Paginate.page(self, request, reserves, self.serializer_class)
        return Response(payload)


class ChangeDeskPriceAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        id = request.data['desk_id']
        try:
            desk_obj = Desk.objects.get(id=id)
        except:
            return Response({'msg': 'desk does not exists'})
        desk_obj.price = request.data['price']
        desk_obj.save()
        return Response({'msg': 'desk price changed'})



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

    def post(self, request):
        payment = request.data['payment']
        if payment:
            payment = True
        else:
            payment = False
        response = ReserveDeskAPI.post(self, request, is_admin=payment)
        print('=admin=================')
        print(response)
        # return Response(response)
        return response

class AdminCancelReservationAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        reserve_id = request.data['reserve_id']
        reserve_obj = Reservation.objects.filter(id=reserve_id).exists()
        reserve_obj.delete()
        return Response({'msg': 'object deleted'})


class Paginate(APIView):
    def page(self, request, queryset, serializer):
        page_number = request.data['page']
        per_page = request.data['per_page']
        # startswith = request.data['startswith']
        paginator = Paginator(queryset, per_page)
        page_range = list(paginator.get_elided_page_range(page_number, on_each_side=3))
        page_obj = paginator.get_page(page_number)
        # data = [{"name": kw} for kw in page_obj.object_list]
        srz_data = serializer(instance=page_obj.object_list, many=True)

        payload = {
            "page": {
                "current": page_obj.number,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            },
            "data": srz_data.data
        }
        print('=========')
        print(payload)
        return payload


class GetUserViaPhoneAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request):
        # phone = request.data['phone_number']
        phone = request.query_params['phone_number']
        print('============')
        print(phone)
        try:
            user = User.objects.filter(phone_number__contains=phone)
        except:
            return Response({'msg': 'user does not exists'})
        srz_data = UserSerializer(instance=user, many=True)
        return Response(srz_data.data)


class GetUsersListAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        filter = UserFilter(request.data, queryset=users)
        # srz_data = UserSerializer(instance=filter.qs, many=True)
        payload = Paginate.page(self, request, filter.qs, self.serializer_class)
        return Response(payload)


class GetQuotes(APIView):
    serializer_class = QuoteSerializer

    def get(self, request):
        quotes = Quotes.objects.all()
        srz_data = self.serializer_class(instance=quotes, many=True)
        return Response(srz_data.data)


class UpdateQuotes(APIView):
    serializer_class = QuoteSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            quote = Quotes.objects.get(id=request.data['id'])
            srz_data.update(quote)
            return Response({'msg': 'updated'})


class GetTodayReservesAPI(APIView):
    serializer_class = ReserveSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        date = request.query_params.get('date')
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        else:
            date = datetime.date.today()
            date = jalali_date.date2jalali(date).strftime('%Y-%m-%d')
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        reservations = Desk.objects.filter(reservation__reservation_time__year=date.year,
                                           reservation__reservation_time__month=date.month,
                                           reservation__reservation_time__day=date.day)

        srz_data = self.serializer_class(instance=reservations, many=True)
        return Response(srz_data.data)

