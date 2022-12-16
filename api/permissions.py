from rest_framework.response import Response
from rest_framework import permissions 
from rest_framework import status

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user:
            message = {
                "error": "unauthorized"
            }
            return Response(message, status=status.HTTP_401_BAD_REQUEST)

        # Instance must have an attribute named `owner`.
        return obj.user == request.user or request.user.is_staff




