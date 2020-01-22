from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='user-signup'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('upload-image/', views.UserImageUploadView.as_view(),
         name='user-image-upload')
]
