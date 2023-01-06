import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Desk, Reservation, User
from .serializers import DeskSerializer, ReserveSerializer
from accounting.permissions import IsNotBanned


class GetReservedDesks(APIView):
    permission_classes = [IsNotBanned, ]
    serializer_class = ReserveSerializer

    def get(self, request):
        if request.data['date']:
            date = request.data['date']
        else:
            date = datetime.today()
        reservations = Desk.objects.filter(reservation__payment=True, reservation__reservation_time=date)
        srz_data = self.serializer_class(reservations, many=True)
        return Response(srz_data.data)


class GetFreeDesks(APIView):
    serializer_class = DeskSerializer

    def get(self, request):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        desks = Desk.objects.all()
        today_reserves = desks.filter(reservation__reservation_time__range=(today_min, today_max))
        today_reserves = today_reserves.filter(reservation__payment=True)
        desks = Desk.objects.exclude(pk__in=today_reserves)
        srz_data = self.serializer_class(instance=desks, many=True)
        return Response(srz_data.data)


class ReserveDeskAPI(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = ReserveSerializer

    def post(self, request):
        reserve_check = {
            'desk': request.data['desk_id'],
            'reservation_time': request.data['day'],
            'status': False
        }

        check = Reservation.objects.filter(**reserve_check)  # IS IT OK ?
        if check:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        srz_data = ReserveSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response({'msg': 'desk reservation completed'})


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
