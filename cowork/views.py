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

    def get(self, request):
        desk_list = Desk.objects.all()
        srz_data = DeskSerializer(instance=desk_list, many=True)
        return Response(srz_data.data)


class CreateDeskAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        srz_data = DeskSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteDeskAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        desk = Desk.objects.filter(pk=pk)
        desk.delete()
        return Response({'msg': 'deleted'})


class DeskListDeleteAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request):
        desk_ids = request.data['desks']
        desks = Desk.objects.filter(id__in=desk_ids)
        for desk in desks:
            desk.delete()
        return Response({'msg': 'desks deleted'})


class GetSpecificDeskAPI(APIView):

    def get(self, desk_id):
        desk = Desk.objects.get(pk=desk_id)
        srz_data = DeskSerializer(instance=desk)
        return Response(srz_data.data)


class FreeDesksListAPI(APIView):
    permission_classes = [IsNotBanned, ]

    def get(self, request):
        desks = Desk.objects.filter(reserved=False)
        srz_data = DeskSerializer(desks, many=True)
        return Response(srz_data.data)


class ReserveDeskAPI(APIView):
    permission_classes = [IsAuthenticated, IsNotBanned]

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

    def get(self, request):
        reservation_obj = Reservation.objects.filter(user__in=request.user)
        srz_data = DeskSerializer(reservation_obj, many=True)
        return Response(srz_data.data)


class GetAllReservesAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        reserves = Reservation.objects.all()
        srz_data = ReserveSerializer(instance=reserves, many=True)
        return Response(srz_data.data)


class GetTodayReservesAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        pass


class GetThisWeekReservesAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        pass


class ChangeDeskPriceAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        desk_obj = get_object_or_404(Desk, id=request.data['desk_id'])
        desk_obj.price = request.data['price']
        desk_obj.save()


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


class GetSpecificDayReservationsAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        date = request.data['date']
        reservations = Reservation.objects.filter(reservation_time=date)
        srz_data = ReserveSerializer(instance=reservations, many=True)
        return Response(srz_data.data)
#
# {
#     '2022-2-34': '7',
#     '2022-2-35': '8',
# }