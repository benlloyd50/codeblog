from django.contrib.auth import get_user_model
from rest_framework import permissions

from .models import BannedUser


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allows owner to update and delete snippets"""

    def has_object_permission(self, request, view, obj):
        """Allows GET requests and when owner the update/delete functionalities"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsNotBanned(permissions.BasePermission):
    """Allows users without the `BANNED` status to make edits and create new things"""

    message = "Banned users may not interact with the data this site"

    def has_permission(self, request, view):
        """Checks to make sure the user is not in the banned list"""
        User = get_user_model()
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return False

        try:
            banned_user = BannedUser.objects.get(user_id=user.pk)
        except BannedUser.DoesNotExist:
            return True

        return banned_user.status != "BANNED"
