from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allow only users in 'admin' group OR Django superusers.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True

        return user.groups.filter(name="admin").exists()

class IsEditor(permissions.BasePermission):
    def has_permission(self, request):
        return request.user.is_authenticated and request.user.groups.filter(name__in=['admin', 'editor']).exists()

class IsViewer(permissions.BasePermission):
    def has_permission(self, request):
        return request.user.is_authenticated