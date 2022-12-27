from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Ban


class IsAdminOrReadOnly(BasePermission):
    message = 'Permission denied; admin only.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_admin


class IsNotBanned(BasePermission):
    message = 'you are banned.'

    def has_permission(self, request, view):
        ban = Ban.objects.filter(user=request.user.id, status=True).exists()
        if not ban:
            return True

        return False
