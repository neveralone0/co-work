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
        else:
            date = datetime.date.today()
            date = jalali_date.date2jalali(date).strftime('%Y-%m-%d')
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        reservations = Desk.objects.filter(reservation__reservation_time__year=date.year,
                                           reservation__reservation_time__month=date.month,
                                           reservation__reservation_time__day=date.day)
        srz_data = DeskSerializer(instance=reservations, many=True)
        return Response(srz_data.data)


class GetFreeDesks(APIView):
    serializer_class = DeskSerializer

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
        free_desks = Desk.objects.exclude(pk__in=reservations)
        srz_data = self.serializer_class(instance=free_desks, many=True)
        return Response(srz_data.data)


class ReserveDeskAPI(APIView):
    # permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = ReserveSerializer

    def post(self, request):
        reserved_desks = list()
        price = int()

        data = request.data
        for key in data:
            print('=data=========')
            print(key)
            print(data[key])
            date = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            try:
                reservations = Desk.objects.get(reservation__reservation_time__year=date.year,
                                                reservation__reservation_time__month=date.month,
                                                reservation__reservation_time__day=date.day,
                                                id=int(data[key]))
                reserved_desks.append(reservations)
            except:
                desk = Desk.objects.get(id=data[key])
                price += desk.price

        print('==========')
        print(price)
        if reserved_desks:
            srz_data = DeskSerializer(instance=reserved_desks, many=True)
            return Response({'msg': 'these desks are reserved for this date',
                             'desks': srz_data.data})

        for key in data:
            date = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            user = User.objects.get(id=request.user.id)
            print('=========')
            print(user)
            desk = Desk.objects.get(id=data[key])
            Reservation.objects.create(
                user=user,
                reservation_time=date,
                desk=desk
            )
            print('=date========')
            print(date)
            # reserve.save()
        return Response({'msg': 'done, reserved'})


# class CancelReservationAPI(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def patch(self, request):
#         reserve_id = request.data['reserve_id']
#         reserve = Reservation.objects.get(id=reserve_id)
#         if reserve.user.id == request.user.id:
#             reserve.status = True
#             reserve.save()
#             return Response({})
#         return Response(status=status.HTTP_400_BAD_REQUEST)


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
