from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions,\
     status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView

from . import serializer
from core import models


class CreateUserView(generics.CreateAPIView):
    """Creates a new user in the system"""
    serializer_class = serializer.CreateUserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = serializer.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = serializer.ManageUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserImageUploadView(APIView):
    """View to upload or view image for user"""
    serializer_class = serializer.TempSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [JSONParser, MultiPartParser]

    def get(self, request, format=None):
        """To get user profile picture"""
        user = get_user_model().objects.get(email=request.user)
        user_profile = models.UserProfile.objects.get(user=user)

        # Preparing the data manually as per our serializer
        data = {'user': {'username': user.username},
                'image': user_profile.image or None}

        # Serializing our prepared data
        ser = serializer.TempSerializer(
            user_profile, data=data, context={"request": request})

        # Returniing appropariate response
        if ser.is_valid():
            return_ser_data = {'id': ser.data.get('id'),
                               'image': ser.data.get('image')}
            return Response(return_ser_data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        """To save the profile picture"""
        user = get_user_model().objects.get(email=request.user)
        user_profile = models.UserProfile.objects.get(user=user)

        # Formatting the data to as per our defined serializer
        data = {'user': {'username': user.username},
                'image': request.data.get('image')}

        # Serializing our data
        ser = serializer.TempSerializer(
            user_profile, data=data, context={"request": request})

        if ser.is_valid():
            if ser.validated_data:
                # Deleting the old image before uploading new image
                if user_profile.image:
                    user_profile.image.delete()

                # Saving the model
                ser.save(user=user)
            return_ser_data = {'id': ser.data.get('id'),
                               'image': ser.data.get('image')}
            return Response(return_ser_data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
