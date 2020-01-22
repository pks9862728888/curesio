from django.urls import path

from . import views

app_name = 'doctor'

urlpatterns = [
    path('signup/', views.CreateDoctorView.as_view(),
         name='doctor-signup'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageDoctorUserView.as_view(), name='me'),
    path('upload-image/', views.DoctorUserImageUploadView.as_view(),
         name='doctor-image-upload')
]
