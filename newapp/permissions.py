
from rest_framework.permissions import BasePermission
class IsShop(BasePermission):
    """
    Custom permission class example.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        """

        if(request.user.is_shop):
            return True
        # Logic to determine if the user has permission.
        # For example, check if the user belongs to a certain group or has specific rights.
        # You can access request.user to get the current user object.
        # You can access request.method to get the HTTP method used in the request.
        
        # For this example, let's just allow all GET requests and restrict others.
        else:
            return False