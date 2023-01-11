from django.urls import path
from finance import views

app_name = 'finance'

urlpatterns = [
    path('pay/<int:order_id>/', views.PayOrderAPI.as_view()),
    path('verify/', views.OrderVerifyAPI.as_view()),
    path('coupon/<int:order_id>/', views.CouponApplyAPI.as_view()),
]