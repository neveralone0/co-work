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

    def get(self, request, is_admin=False):
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

    def post(self, request, is_admin=False):
        reserved_desks = list()
        price = int()
        count = int()
        data = request.data
        data = data.copy()
        payment = data['payment']
        del(data['payment'])
        user = data['phone_number']
        del(data['phone_number'])
        try:
            user = User.objects.get(id=user)
        except:
            user = request.user.id
            user = User.objects.get(id=user)
        print('=============thedata')
        
        for key in data:
            # num = 0
            # for i in data[key]:
            #     num += 1
            #     if num > 3:
            #         return Response({'msg': 'date is duplicated (you can reserve 1 desk per day)'})
            # num = 0

            date = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            try:
                check_today_reservation = User.objects.get(reservation__reservation_time__year=date.year,
                                                           reservation__reservation_time__month=date.month,
                                                           reservation__reservation_time__day=date.day,
                                                           id=user)

                if check_today_reservation:
                    return Response({'msg': 'you can reserve 1 desk per day'})
            except: pass

            try:
                reservations = Desk.objects.get(reservation__reservation_time__year=date.year,
                                                reservation__reservation_time__month=date.month,
                                                reservation__reservation_time__day=date.day,
                                                id=int(data[key]))
                reserved_desks.append(reservations)
            except:
                desk = Desk.objects.get(id=data[key])
                count += 1
                price += desk.price

        if reserved_desks:
            srz_data = DeskSerializer(instance=reserved_desks, many=True)
            return Response({'msg': 'these desks are reserved for this date',
                             'desks': srz_data.data})

        if count >= 20:
            price -= 5*count
        elif count >= 10:
            price -= 3*count

        for key in data:
            date = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            desk = Desk.objects.get(id=data[key])
            Reservation.objects.create(
                user=user,
                reservation_time=date,
                desk=desk
            )

            if is_admin:
                payment = True
            else:
                payment = False
        return Response({'msg': 'done, reserved',
                         'price': price,
                         'payment': payment})


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
    serializer_class = ReserveSerializer

    def get(self, request):
        reservation_obj = Reservation.objects.filter(user=request.user.id)
        srz_data = self.serializer_class(reservation_obj, many=True)
        return Response(srz_data.data)


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
