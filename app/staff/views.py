from rest_framework import generics, authentication, permissions

from . import serializer


class IsStaffUser(permissions.BasePermission):
    """Allows access to only staff user."""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class ProcedureView(generics.ListCreateAPIView,
                    generics.RetrieveUpdateAPIView):
    """View for creating, adding or deleting procedure"""
    serializer_class = serializer.ProcedureSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (IsStaffUser, )
