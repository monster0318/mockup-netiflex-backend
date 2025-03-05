from rest_framework import permissions



class IsAdminOrNotModify(permissions.BasePermission):
    """Only admin or staff members can delete, put and post,
       other authenticated users can retrieve and list videos"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_superuser)
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_superuser)