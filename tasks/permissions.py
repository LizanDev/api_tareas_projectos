from rest_framework import permissions


class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    """Allow only project owner to modify tasks, authenticated users can read."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.project.owner == request.user
