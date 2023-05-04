from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return (request.method in permissions.SAFE_METHODS
                    or request.user.is_admin)
        except AttributeError:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            return (request.method in permissions.SAFE_METHODS
                    or request.user.is_admin)
        except AttributeError:
            return False


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.is_admin
                or request.user.is_moderator)
