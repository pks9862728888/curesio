from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'staff'

router = DefaultRouter()
router.register('procedure', views.ProcedureViewSet)

urlpatterns = [
     path('', include(router.urls)),
]
