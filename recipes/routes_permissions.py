from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj) -> bool:
        """Verify if the user has permission"""
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user

    def has_permission(self, request, view) -> bool:
        """Verify if the user has permission"""
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated
