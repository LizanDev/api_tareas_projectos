from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow only owner to modify, authenticated users can read."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
