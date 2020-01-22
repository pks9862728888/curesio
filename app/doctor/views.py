from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import generics, authentication, permissions,\
    status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView

from . import serializer
from core import models


def check_file_size_limit(picture_size, size_limit):
    """
    Returns true if the image has valid size limit.

    size_limit: in bytes
    """
    if picture_size > size_limit:
        return False
    else:
        return True


class CreateDoctorView(generics.CreateAPIView):
    """Creates a new user in the system"""
    serializer_class = serializer.CreateDoctorSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = serializer.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageDoctorUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated doctor"""
    serializer_class = serializer.ManageDoctorUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """Retrieve and return authenticated doctor user"""
        return self.request.user


class DoctorUserImageUploadView(APIView):
    """View to upload or view image for doctor"""
    serializer_class = serializer.DoctorImageUploadSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [JSONParser, MultiPartParser]

    def get(self, request, format=None):
        """To get user profile picture"""
        doctor = get_user_model().objects.get(email=request.user)
        user_profile = models.UserProfile.objects.get(user=doctor)

        # Preparing the data manually as per our serializer
        data = {'user': {'username': doctor.username},
                'image': user_profile.image or None}

        # Serializing our prepared data
        ser = serializer.DoctorImageUploadSerializer(
            user_profile, data=data, context={"request": request})

        # Returning appropariate response
        if ser.is_valid():
            return_ser_data = {'id': ser.data.get('id'),
                               'image': ser.data.get('image')}
            return Response(return_ser_data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        """To save the profile picture"""
        doctor = get_user_model().objects.get(email=request.user)
        user_profile = models.UserProfile.objects.get(user=doctor)

        # Formatting the data to as per our defined serializer
        data = {'user': {'username': doctor.username},
                'image': request.data.get('image')}

        # Serializing our data
        ser = serializer.DoctorImageUploadSerializer(
            user_profile, data=data, context={"request": request})

        if ser.is_valid():
            if ser.validated_data:
                # Checking for size limit of uploaded file(max 2 Mb)
                # Converting 20Mb = 20 * 1024 * 1024 bytes = 20971520 bytes
                if not check_file_size_limit(request.data.get('image').size,
                                             size_limit=20971520):
                    msg = _('File size too large. Maximum allowed size: 20 Mb')
                    res = {'image': [msg]}
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

                # Deleting the old image before uploading new image
                if user_profile.image:
                    user_profile.image.delete()

                # Saving the model
                ser.save(user=doctor)
            return_ser_data = {'id': ser.data.get('id'),
                               'image': ser.data.get('image')}
            return Response(return_ser_data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
