from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allows owner to update and delete snippets"""

    def has_object_permission(self, request, view, obj):
        """Allows GET requests and when owner the PUT and DELETE"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
