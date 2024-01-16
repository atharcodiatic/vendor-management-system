from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerAction(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        else:
            return request.method in permissions.SAFE_METHODS
    
    

    