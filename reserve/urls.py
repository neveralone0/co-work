from django.urls import path
from reserve import views

app_name = 'reserve'

urlpatterns = [

    path('free-desks/', views.GetFreeDesks.as_view()),
    path('reserved-desks/', views.GetReservedDesks.as_view()),
    path('get-desks/', views.GetDesks.as_view()),

    path('reserve-desk/', views.ReserveDeskAPI.as_view()),
    path('my-reservations/', views.MyReservationsAPI.as_view()),
    # path('my-receipts/', views.GetMyReceipts.as_view()),

    # path('check/', views.Check.as_view()),
]