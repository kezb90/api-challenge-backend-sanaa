# document/permissions.py
from rest_framework.permissions import BasePermission

class DocumentPermission(BasePermission):
    """
    Uses Django's permissions:
    - view_document
    - add_document
    - change_document
    - delete_document
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        method = request.method

        if method in ("GET", "HEAD", "OPTIONS"):
            return user.has_perm("document.view_document")

        if method == "POST":
            return user.has_perm("document.add_document")

        if method in ("PUT", "PATCH"):
            return user.has_perm("document.change_document")

        if method == "DELETE":
            return user.has_perm("document.delete_document")

        return False
