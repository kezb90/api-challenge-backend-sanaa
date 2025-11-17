from rest_framework import permissions

class DocumentPermission(permissions.BasePermission):
    """
    Roles:
    - viewer: can read only
    - editor: can upload and update, but cannot delete
    - admin: full access
    """

    def has_permission(self, request, view):
        user = request.user
        
        if not user.is_authenticated:
            return False

        role = user.role  # from User model property

        if request.method in permissions.SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS

        if request.method == "POST":
            return role in ["editor", "admin"]

        if request.method in ["PUT", "PATCH"]:
            return role in ["editor", "admin"]

        if request.method == "DELETE":
            return role == "admin"

        return False
