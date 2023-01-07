import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Desk, Reservation, User
from .serializers import DeskSerializer, ReserveSerializer
from accounting.permissions import IsNotBanned
import jalali_date


class GetReservedDesks(APIView):
    permission_classes = [IsNotBanned, ]
    serializer_class = ReserveSerializer

    def get(self, request):
        date = request.query_params.get('date')
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            date = jalali_date.date2jalali(date).strftime('%Y-%m-%d')
            print('=====')
            print(date)
        else:
            # date = datetime.date.today()
            date = datetime.datetime.today()
            date = jalali_date.date2jalali(date).strftime('%y-%m-%d')
            print('============')
            print(date)
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        print('====================================================')
        print(date)
        rz = Reservation.objects.all()
        print(rz[1].reservation_time.date())
        reservations = Desk.objects.filter(reservation__reservation_time__year=date.year,
                                           reservation__reservation_time__month=date.month,
                                           reservation__reservation_time__day=date.day)
        print('=================')
        print(reservations)
        srz_data = self.serializer_class(reservations, many=True)
        return Response(srz_data.data)


class GetFreeDesks(APIView):
    serializer_class = DeskSerializer

    def get(self, request):
        if request.query_params['date']:
            date = request.query_params['date']
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        else:
            date = datetime.date.today()
        today_reserves = Desk.objects.filter(reservation__reservation_time__day=date)
        free_desks = Desk.objects.exclude(pk__in=today_reserves)
        srz_data = self.serializer_class(instance=free_desks, many=True)
        print('=======')
        print(min)
        return Response(srz_data.data)


class ReserveDeskAPI(APIView):
    # permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = ReserveSerializer

    def post(self, request):
        for day, desk in request.data:
            day_min = datetime.datetime.combine(day, datetime.time.min)
            day_max = datetime.datetime.combine(day, datetime.time.max)
            reserved_desks = Desk.objects.get(reservation__reservation_time__range=(day_min, day_max),
                                              id=desk)
            if reserved_desks:
                reserved_desks.append(reserved_desks)
        if reserved_desks:
            srz_data = DeskSerializer(instance=reserved_desks, many=True)
            return Response({'msg': 'this desks are reserved for this date',
                             'days': srz_data.data})
        price = int()
        for desk in request.data:
            price += desk.price

        for k, w in request.data:
            reserve = Reservation.objects.create()
            reserve.user = request.user.id
            reserve.reservation_time = k
            reserve.desk = w
            reserve.save()

        return Response({'msg': 'done'})


class CancelReservationAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        reserve_id = request.data['reserve_id']
        reserve = Reservation.objects.get(id=reserve_id)
        if reserve.user.id == request.user.id:
            reserve.status = True
            reserve.save()
            return Response({})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CurrentUserReservationsAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = DeskSerializer

    def get(self, request):
        reservation_obj = Reservation.objects.filter(user__in=request.user)
        srz_data = DeskSerializer(reservation_obj, many=True)
        return Response(srz_data.data)


class GetTodayReservesAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        pass


class GetSpecificDayReservationsAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReserveSerializer

    def post(self, request):
        date = request.data['date']
        reservations = Reservation.objects.filter(reservation_time=date)
        srz_data = ReserveSerializer(instance=reservations, many=True)
        return Response(srz_data.data)


class Check(APIView):
    def post(self, request):
        date = request.data['date']
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        # user .date() on db object......
        if datetime.date.today() == date:
            print('+++++++++++++++++++++++++++++')
            print('amazing:D')