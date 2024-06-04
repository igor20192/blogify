from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """A permission class that checks whether the user is the author of an object or an administrator.

    Methods:
    - has_object_permission: Checks if the user has permission to perform an operation on a particular object.
    """

    def has_object_permission(self, request, view, obj):
        """Checks whether the user has permission to perform an operation on a particular object.

        Parameters:
        - request: HttpRequest object.
        - view: The View object that is executing the current request.
        - obj: The object on which the operation is performed.

        Returns:
        - True if the user is the author of the object or an administrator. Otherwise, False.
        """
        return request.user == obj.author or request.user.is_staff
