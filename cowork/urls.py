from django.urls import path
from cowork import views

app_name = 'cowork'

urlpatterns = [
    path('get-desks/', views.GetDeskAPI.as_view()),
    path('get-desk/<int:desk_ip>/', views.GetSpecificDeskAPI.as_view()),

    path('create-desk/', views.CreateDeskAPI.as_view()),

    path('delete-desk/<int:pk>/', views.DeleteDeskAPI.as_view()),
    path('delete-desks/', views.DeskListDeleteAPI.as_view()),

    path('free-desks/', views.FreeDesksListAPI.as_view()),

    path('reserve-desk/', views.ReserveDeskAPI.as_view()),
    path('cancle-reserve/', views.CancelReservationAPI.as_view()),
    path('my-reservations/', views.CurrentUserReservationsAPI.as_view()),
    path('all-reservations/', views.GetAllReservesAPI.as_view()),

    path('change-desk-price/', views.ChangeDeskPriceAPI.as_view()),
    path('change-multidesk-price/', views.ChangeMultiDesksPriceAPI.as_view()),
    path('change-alldesks-price/', views.ChangeAllDesksPriceAPI.as_view()),

    path('admin-reserve/', views.AdminReserveDeskAPI.as_view()),
    path('admin-cancel-reserve/', views.AdminCancelReservationAPI.as_view()),
]