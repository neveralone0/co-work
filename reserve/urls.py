from django.urls import path
from reserve import views

app_name = 'reserve'

urlpatterns = [
    path('get-desks/', views.GetDeskAPI.as_view()),
    path('get-desk/<int:desk_id>/', views.GetSpecificDeskAPI.as_view()),

    path('free-desks/', views.FreeDesksListAPI.as_view()),

    path('reserve-desk/', views.ReserveDeskAPI.as_view()),
    path('cancle-reserve/', views.CancelReservationAPI.as_view()),
    path('my-reservations/', views.CurrentUserReservationsAPI.as_view()),

]