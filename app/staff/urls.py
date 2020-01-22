from django.urls import path

from . import views

app_name = 'staff'

urlpatterns = [
     path('procedure/', views.ProcedureView.as_view(), name='procedure-add'),
]
