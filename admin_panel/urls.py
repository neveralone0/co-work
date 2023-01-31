from django.urls import path, include
from admin_panel import views
from reserve.views import GetSpecificDayReservationsAPI
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('image', views.MyModelViewSet, basename='imageee')

app_name = 'admin'
urlpatterns = [
    path('', include(router.urls)),
    path('get-all-images/', views.GetAllImage.as_view()),
    path('upload-image/', views.UploadImage.as_view()),
    path('delete-image/', views.DeleteImage.as_view()),
    path('list-delete-image/', views.ListDeleteImages.as_view()),

    path('contact-us/', views.ContactUsAPI.as_view()),
    # path('contactus-update/', views.ContactUsUpdate.as_view()),

    path('card/', views.CardAPI.as_view()),

    path('ban-user/', views.BanUserAPI.as_view()),
    path('unban-user/', views.UnbanUserAPI.as_view()),
    path('current-bans/', views.CurrentlyBannedUsersAPI.as_view()),
    path('user-ban-history/', views.UserBanHistoryAPI.as_view()),
    path('user-ban-status/', views.UserBanStatusAPI.as_view()),
    path('ban-history/', views.BanHistoryAPI.as_view()),

    path('get-desk/<int:desk_id>/', views.GetSpecificDeskAPI.as_view()),
    path('create-desk/', views.CreateDeskAPI.as_view()),
    # path('delete-desk/', views.DeleteDeskAPI.as_view()),
    path('delete-desks/', views.DeskDeleteAPI.as_view()),


    path('change-desk-price/', views.ChangeDeskPriceAPI.as_view()),
    path('change-multidesk-price/', views.ChangeMultiDesksPriceAPI.as_view()),
    path('change-alldesks-price/', views.ChangeAllDesksPriceAPI.as_view()),

    path('reserve/', views.AdminReserveDeskAPI.as_view()),
    # path('admin-cancel-reserve/', views.AdminCancelReservationAPI.as_view()),

    path('all-reservations/', views.GetAllReservesAPI.as_view()),
    path('get-reservations-via-date/', views.GetTodayReservesAPI.as_view()),
    path('get-reservations/', GetSpecificDayReservationsAPI.as_view()),


    path('get-all-users/', views.GetUsersListAPI.as_view()),
    path('get-user-by-phone/', views.GetUserViaPhoneAPI.as_view()),

    path('get-quotes/', views.GetQuotes.as_view()),
    path('update-quotes/', views.UpdateQuotes.as_view()),
    #
    # path('get-all-income/', views.GetAllIncome.as_view()),
    # path('get-month-income/', views.GetMonthIncome.as_view()),

    path('remove-user/', views.RemoveUserAPI.as_view()),
]


# urlpatterns += router.urls
