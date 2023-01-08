from django.urls import path
from reserve import views

app_name = 'reserve'

urlpatterns = [

    path('free-desks/', views.GetFreeDesks.as_view()),
    path('reserved-desks/', views.GetReservedDesks.as_view()),

    path('reserve-desk/', views.ReserveDeskAPI.as_view()),
    # path('cancle-reserve/', views.CancelReservationAPI.as_view()),
    path('my-reservations/', views.CurrentUserReservationsAPI.as_view()),

    path('check/', views.Check.as_view()),
]