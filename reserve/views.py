from datetime import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Desk, Reservation, User
from .serializers import DeskSerializer, ReserveSerializer
from accounting.permissions import IsNotBanned


class GetDeskAPI(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]
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


class FreeDesksListAPI(APIView):
    permission_classes = [IsNotBanned, ]
    serializer_class = DeskSerializer

    def get(self, request):
        desks = Desk.objects.filter(reserved=False)
        srz_data = DeskSerializer(desks, many=True)
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
