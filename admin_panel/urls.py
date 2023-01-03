from django.urls import path, include
from admin_panel import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('image', views.MyModelViewSet, basename='imageee')

app_name = 'admin'

urlpatterns = [
    path('', include(router.urls)),
    path('get-all-images/', views.GetAllImage.as_view()),
    path('upload-image/', views.UploadImage.as_view()),
    # path('upload-image/', views.ImageViewSet.as_view()),
    path('delete-image/', views.DeleteImage.as_view()),
    path('list-delete-image/', views.ListDeleteImages.as_view()),

    path('contactus/', views.ContactUsGet.as_view()),
    path('contactus-update/', views.ContactUsUpdate.as_view()),

    path('card/', views.CardAPI.as_view()),

    path('ban-user/', views.BanUserAPI.as_view()),
    path('unban-user/', views.UnbanUserAPI.as_view()),
    path('current-bans/', views.CurrentlyBannedUsersAPI.as_view()),
    path('user-ban-history/', views.UserBanHistoryAPI.as_view()),
    path('user-ban-status/', views.UserBanStatusAPI.as_view()),

    path('create-desk/', views.CreateDeskAPI.as_view()),
    path('delete-desk/<int:desk_id>/', views.DeleteDeskAPI.as_view()),
    path('delete-desks/', views.DeskListDeleteAPI.as_view()),

    path('change-desk-price/', views.ChangeDeskPriceAPI.as_view()),
    path('change-multidesk-price/', views.ChangeMultiDesksPriceAPI.as_view()),
    path('change-alldesks-price/', views.ChangeAllDesksPriceAPI.as_view()),

    path('admin-reserve/', views.AdminReserveDeskAPI.as_view()),
    path('admin-cancel-reserve/', views.AdminCancelReservationAPI.as_view()),

    path('all-reservations/', views.GetAllReservesAPI.as_view()),

]

# urlpatterns += router.urls
