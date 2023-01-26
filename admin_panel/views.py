import datetime
import jalali_date
from django.core.paginator import Paginator
from rest_framework.views import APIView, Response, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from accounting.serializers import UserSerializer
from reserve.views import ReserveDeskAPI
from reserve.models import Reservation, Desk
from accounting.serializers import UserListSerializer
from reserve.serializers import ReserveSerializer, DeskSerializer, GetReserveSerializer
from .serializers import *
from .models import *
from utils import UserFilter


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
    """
    body{\n
    id
    }
    """
    def delete(self, request):
        id = request.data['id']
        img = Images.objects.filter(id=id)
        img.delete()
        return Response({'msg': 'deleted'})


class ListDeleteImages(APIView):
    """
    body{\n
    ids = array of ids
    }
    """
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
        """
        body{\n
        }
        """
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
    """
    body{\n
    user = (user id)
    }
    """
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BanSerializer

    def post(self, request):
        srz_data = BanSerializer(data=request.data)
        if srz_data.is_valid():
            user = request.data['user']
            try:
                check = User.objects.filter(bans__status=True, id=user).exists()
                if check:
                    return Response({'msg': 'user already banned!'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({'msg': 'user not found!'}, status=status.HTTP_400_BAD_REQUEST)
            srz_data.create(validated_data=srz_data.validated_data)
            return Response({'msg': 'user banned'})


class UnbanUserAPI(APIView):
    """
    body{\n
    user = (user id)
    }
    """
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
    """
    body{\n
    user = (user id)
    }
    """
    # permission_classes = [IsAuthenticated, ]
    serializer_class = BanSerializer

    def post(self, request):
        user = request.data['user']
        ban_history = Ban.objects.filter(user=user)
        # srz_data = BanSerializer(instance=ban_history, many=True)
        payload = Paginate.page(self, request, ban_history, self.serializer_class)
        return Response(payload)


class UserBanStatusAPI(APIView):
    """
    body{\n
    user = (user id)
    }
    """
    # permission_classes = [IsAuthenticated, ]
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


class GetSpecificDeskAPI(APIView):
    serializer_class = DeskSerializer

    def get(self, desk_id):
        desk = Desk.objects.get(pk=desk_id)
        srz_data = DeskSerializer(instance=desk)
        return Response(srz_data.data)


class CreateDeskAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    # serializer_class = DeskSerializer

    def post(self, request):
        srz_data = DeskSerializer(data=request.data)
        if srz_data.is_valid():
            type = request.data['type']
            if type == 'group':
                srz_data.validated_data['is_group'] = True
            elif type == 'single':
                srz_data.validated_data['is_group'] = False
            srz_data.save()
            return Response({'msg': 'created'})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeskDeleteAPI(APIView):
    """
    body{\n
    groups = int \n
    singles = int \n
    }
    """
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        groups = request.data['groups']
        singles = request.data['singles']
        single_desks = Desk.objects.filter(is_group=False)[:int(singles)]
        group_desks = Desk.objects.filter(is_group=True)[:int(groups)]
        for desk in single_desks:
            desk.delete()
        for desk in group_desks:
            desk.delete()
        return Response({'msg': 'desks deleted'})


class GetAllReservesAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GetReserveSerializer

    def post(self, request):
        reserves = Reservation.objects.all().order_by('reservation_time')
        # srz_data = ReserveSerializer(instance=reserves, many=True)
        payload = Paginate.page(self, request, reserves, self.serializer_class)
        return Response(payload)


class ChangeDeskPriceAPI(APIView):
    """
    body{\n
    desk_id, price
    }
    """
    # permission_classes = [IsAuthenticated, IsAdminUser]

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
    """
    body{\n
    desk_list (array of desk ids)\n
    }
    """
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        desk_list = Desk.objects.filter(id__in=request.data['desk_list'])
        price = request.data['price']
        for desk in desk_list:
            desk.price = price
            desk.save()


class ChangeAllDesksPriceAPI(APIView):
    """
    body{\n
    price
    }
    """
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        desk_list = Desk.objects.all()
        price = request.data['price']
        for desk in desk_list:
            desk.price = price
            desk.save()
        return Response({'msg': 'done'})


class AdminReserveDeskAPI(APIView):
    """
    body{\n
    +++++++++++++++++++++++++++++++++++++
    ONLY:\n
    payment = boolean (offline payment if false)\n
    phone_number = user phone...\n
    key values...\n
    {1401-01-01: 12},{1401-01-02: 12}
    }
    """
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        payment = True
        response = ReserveDeskAPI.post(self, request, is_admin=payment)
        return response

# class AdminCancelReservationAPI(APIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#
#     def post(self, request):
#         reserve_id = request.data['reserve_id']
#         reserve_obj = Reservation.objects.filter(id=reserve_id).exists()
#         reserve_obj.delete()
#         return Response({'msg': 'object deleted'})


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
                "total": paginator.num_pages
            },
            "data": srz_data.data
        }
        return payload


class GetUserViaPhoneAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    """
    body{\n
    phone_number
    }
    """
    serializer_class = UserSerializer

    def get(self, request):
        # phone = request.data['phone_number']
        phone = request.query_params['phone_number']
        try:
            user = User.objects.filter(phone_number__contains=phone)
        except:
            return Response({'msg': 'user does not exists'})
        srz_data = UserSerializer(instance=user, many=True)
        return Response(srz_data.data)


class GetUsersListAPI(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserListSerializer

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
    """
    body{\n
    id
    }
    """
    serializer_class = QuoteSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            quote = Quotes.objects.get(id=request.data['id'])
            srz_data.update(quote)
            return Response({'msg': 'updated'})


class GetTodayReservesAPI(APIView):
    """
    body{\n
    date = 1401-01-01
    }
    """
    serializer_class = ReserveSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        date = request.data['date']
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
#
#
# class GetAllIncome(APIView):
#     serializer_class = ReserveSerializer
#
#     def post(self, request):
#         income = Reservation.objects.all()
#         srz_data = self.serializer_class(instance=income, many=True)
#         return Response(srz_data.data)
#
#
# class GetMonthIncome(APIView):
#     serializer_class = IncomeSerializer
#
#     def post(self, request):
#         date = datetime.date.today()
#         date = jalali_date.date2jalali(date).strftime('%Y-%m-%d')
#         date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
#
#         income = Income.objects.filter(date__month=date.month)
#         srz_data = self.serializer_class(instance=income, many=True)
#         return Response(srz_data.data)


class RemoveUserAPI(APIView):
    """
    body{\n
    user_id = int
    }
    """
    # permission_classes = [IsAdminUser, IsAdminUser]

    def post(self, request):
        user_id = request.data['user_id']
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return Response({'message': 'user deleted successfully'}, status=status.HTTP_200_OK)
