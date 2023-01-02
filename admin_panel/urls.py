from django.urls import path
from admin_panel import views

app_name = 'admin'
urlpatterns = [
    path('get-all-images/', views.GetAllImage.as_view()),
    path('upload-image/', views.UploadImage.as_view()),
    path('delete-image/', views.DeleteImage.as_view()),
    path('list-delete-image/', views.ListDeleteImages.as_view()),

    path('contactus/', views.ContactUsGet.as_view()),
    path('contactus-update/', views.ContactUsUpdate.as_view()),

    path('card/', views.CardAPI.as_view()),
    # path('card/', views.CardAPI.as_view()),

    # path('add-li/', views.AddLi.as_view()),
    # path('update-li/<int:pk>', views.UpdateLi.as_view()),
    # path('delete-li/<int:pk>', views.DeleteLi.as_view()),
]