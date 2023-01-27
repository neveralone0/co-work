import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Desk, Reservation, User
from .serializers import DeskSerializer, ReserveSerializer, FreeDeskSerializer, MyReserveSerializer
from accounting.permissions import IsNotBanned
from utils import ReserveFilter
import jalali_date


class GetReservedDesks(APIView):
    # permission_classes = [IsNotBanned, ]
    serializer_class = ReserveSerializer

    def post(self, request):
        """
        body{\n
        date = 1401-01-01 \n
        NOTE: by default returns TODAY if empty
        }
        """
        data = request.data
        free_resp = dict()
        for d in data:
            date = datetime.datetime.strptime(data[d], "%Y-%m-%d").date()
            reservations = Desk.objects.filter(reservation__reservation_time__year=date.year,
                                               reservation__reservation_time__month=date.month,
                                               reservation__reservation_time__day=date.day)
            srz_data = DeskSerializer(instance=reservations, many=True)
            free_resp[d] = srz_data.data
        return Response(free_resp)


class GetFreeDesks(APIView):
    """
    body{\n
    date = 1401-01-01 \n
    NOTE: by default returns TODAY if empty
    }
    """
    serializer_class = FreeDeskSerializer

    def post(self, request, is_admin=False):
        data = request.data
        full_days_single = list()
        full_days_group = list()
        for d in data:
            date = datetime.datetime.strptime(data[d], "%Y-%m-%d").date()
            reservations = Desk.objects.filter(reservation__reservation_time__year=date.year,
                                               reservation__reservation_time__month=date.month,
                                               reservation__reservation_time__day=date.day)

            free_desks_single = Desk.objects.exclude(pk__in=reservations, is_group=True)
            free_desks_group = Desk.objects.exclude(pk__in=reservations, is_group=False)
            if not free_desks_single:
                full_days_single = data[d]
            if not free_desks_group:
                full_days_group = data[d]

        if not full_days_single and full_days_group:
            return Response({'msg': True})
        else:
            return Response({'msg': False,
                             'full_days_group': full_days_group,
                             'full_days_single': full_days_single})


class ReserveDeskAPI(APIView):
    """
    body{\n
    {1401-01-01: 12},{1401-01-02: 12}
    }
    """

    # permission_classes = [IsAuthenticated, IsNotBanned]
    # serializer_class = ReserveSerializer

    def post(self, request, is_admin=False):
        reserve_status = False
        reserved_desks = dict()
        price = int()
        single_count = int()
        group_count = int()
        data = request.data
        data = data.copy()
        try:
            user = data['phone_number']
            del (data['phone_number'])
        except:
            pass
        try:
            user = User.objects.get(id=user)
        except:
            user = request.user.id
            user = User.objects.get(id=user)

        now = datetime.date.today()
        now = jalali_date.date2jalali(now).strftime('%Y-%m-%d')
        now = datetime.datetime.strptime(now, "%Y-%m-%d").date()

        for key in data:
            date = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            if date < now:
                print(now)
                return Response({'msg': 'you cant reserve in past!'})
            try:
                check_today_reservation = User.objects.get(reservation__reservation_time__year=date.year,
                                                           reservation__reservation_time__month=date.month,
                                                           reservation__reservation_time__day=date.day,
                                                           id=user.id)
                if check_today_reservation:
                    return Response({'msg': 'you can reserve 1 desk per day'})
            except:
                pass

            try:
                if data[key] == 'single':
                    type = False
                else:
                    type = True
                print(type)
                print(not type)
                reservations = Desk.objects.filter(reservation__reservation_time__year=date.year,
                                                   reservation__reservation_time__month=date.month,
                                                   reservation__reservation_time__day=date.day,
                                                   is_group=type)
                free_desks = Desk.objects.exclude(pk__in=reservations)
                free_desks = free_desks.exclude(is_group=(not type))
                if free_desks:
                    if data[key] == 'group':
                        group_count += 1
                        price += 50
                    elif data[key] == 'single':
                        single_count += 1
                        price += 30
                else:
                    reserved_desks[key] = data[key]
                    reserve_status = True
            except Exception as e:
                print(e)

        if reserve_status:
            print(reserve_status)
            # srz_data = DeskSerializer(instance=reserved_desks, many=True)
            return Response({'msg': 'these dates are full',
                             'dates': reserved_desks})
        print('we r not here')
        if (single_count + group_count) >= 20:
            price -= 5 * (single_count + group_count)
        elif (single_count + group_count) >= 10:
            price -= 3 * (single_count + group_count)

        for key in data:
            if data[key] == 'group':
                group = True
            else:
                group = False
            date = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            reservations = Desk.objects.filter(reservation__reservation_time__year=date.year,
                                               reservation__reservation_time__month=date.month,
                                               reservation__reservation_time__day=date.day)
            free_desks = Desk.objects.exclude(pk__in=reservations)
            Reservation.objects.create(
                user=user,
                reservation_time=date,
                desk=free_desks[0],
                is_group=group,
                price=free_desks[0].price,
            )

            if is_admin:
                payment = True
            else:
                payment = False

        return Response({'msg': 'done, reserved',
                         'price': price,
                         'payment': payment})


class MyReservationsAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyReserveSerializer

    def post(self, request):
        reservation_obj = Reservation.objects.filter(user=request.user.id).order_by('reservation_time')
        payload = Paginate.page(self, request, reservation_obj, self.serializer_class)
        return Response(payload)


class GetSpecificDayReservationsAPI(APIView):
    """
    body{\n
    date = 1401-1-1
    }
    """
    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReserveSerializer

    def post(self, request):
        # date = request.data['date']
        reservations = Reservation.objects.all()
        filter = ReserveFilter(request.data, reservations)
        # reservations = Reservation.objects.filter(reservation_time=date)
        # srz_data = ReserveSerializer(instance=filter.qs, many=True)
        payload = Paginate.page(self, request, filter.qs, self.serializer_class)
        return Response(payload)


class Check(APIView):
    def post(self, request):
        date = request.data['date']
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        # user .date() on db object......
        if datetime.date.today() == date:
            print('+++++++++++++++++++++++++++++')
            print('amazing:D')


class GetDesks(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DeskSerializer

    def get(self, request):
        g_desks = Desk.objects.filter(is_group=True)
        s_desks = Desk.objects.filter(is_group=False)
        g_srz_data = DeskSerializer(instance=g_desks, many=True)
        s_srz_data = DeskSerializer(instance=s_desks, many=True)
        return Response({'singles': s_srz_data.data, 'groups': g_srz_data.data})


# class GetMyReceipts(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         id = request.user.id
#         user = User.objects.get(id=id)
#         receipts = Income.objects.filter(user=user)
#         srz_data = ReceiptSerializer(instance=receipts, many=True)
#         return Response(srz_data.data)


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
