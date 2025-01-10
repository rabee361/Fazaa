from rest_framework.permissions import BasePermission
from users.models import Client, Shareek

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if not Client.objects.get(user=request.user).exists():
            return False
        return request.user.user_type.name == 'client'


class IsShareekUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type == 'shareek'


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type.name == 'admin'

