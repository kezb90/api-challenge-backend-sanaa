from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.groups.filter(name='admin').exists()
        )

class IsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name__in=['admin', 'editor']).exists()

class IsViewer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated