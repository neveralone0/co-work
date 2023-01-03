from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounting import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('update-user-info', views.UpdateUserInfo, basename='update-user-info')


app_name = 'accounting'
urlpatterns = [
    path('', include(router.urls)),
    # path('user-role/', views.UserRoleAPI.as_view()),
    path('register/', views.RegisterUser.as_view()),
    path('request-code/', views.SendOTPCodeAPI.as_view()),
    path('verify-code/', views.VerifyOtpCodeAPI.as_view()),
    # path('update-user-info/', views.UpdateUserInfo.as_view()),
    # path('login/', views.VerifyOtpCodeAPI.as_view()),
    path('remove-user/<int:user_id>/', views.RemoveUserAPI.as_view()),

    path('get-working-category/', views.GetWorkingCategory.as_view()),

    # path('reset-password/', views.ResetPasswordAPI.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', views.LogoutView.as_view(), name='auth_logout'),

    path('ban-user/', views.BanUserAPI.as_view()),
    path('unban-user/', views.UnbanUserAPI.as_view()),
    path('current-banns/', views.CurrentlyBannedUsersAPI.as_view()),
    path('user-ban-history/', views.CurrentUserBanHistoryAPI.as_view()),
    path('user-ban-status/', views.CurrentUserBanStatusAPI.as_view()),

    path('get-all-users/', views.GetUsersListAPI.as_view()),
    path('get-user-by-phone/', views.GetUserViaPhoneAPI.as_view()),

    path('delete-all-codes/', views.RemoveAllCodes.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
