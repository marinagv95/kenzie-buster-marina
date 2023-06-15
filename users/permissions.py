from rest_framework import exceptions
from rest_framework import permissions
from rest_framework.views import View, Request
from rest_framework.views import exception_handler


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_employee
        )
    
class CustomIsAuthenticated(permissions.BasePermission):
    message = 'Authentication credentials were not provided.'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed(self.message)

        return True
    
    def render(self, request, exception):
        if isinstance(exception, exceptions.AuthenticationFailed):
            response = exception_handler(exception, {})
            response.status_code = 401
            return response

        return None
    

class UserAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_employee:
            return True

        if request.method == 'GET' and obj == request.user:
            return True

        return False
