from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _

from rest_framework import authentication, permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from . import serializer
from core import models


class IsStaffOrReadOnly(permissions.BasePermission):
    """Allows superuser access to staff else read only access"""

    def has_permission(self, request, view):
        # safe methods are get, head and options requests
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
        else:
            return False


class ProcedureViewSet(ModelViewSet):
    """Manage procedure in database by staff users"""
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (IsStaffOrReadOnly, )
    queryset = models.Procedure.objects.all()
    serializer_class = serializer.ProcedureSerializer

    def get_queryset(self):
        """Return queryset ordered by name"""
        return self.queryset.order_by("-name")

    def create(self, request, *args, **kwargs):
        """Overriding create method to raise integrity error"""
        try:
            return super(ProcedureViewSet, self).create(request,
                                                        *args, **kwargs)
        except IntegrityError:
            msg = {'name': _('Procedure with this name already exists.')}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
