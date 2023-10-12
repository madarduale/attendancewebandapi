from rest_framework.permissions import BasePermission

class IsTeacherOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_teacher or request.user.is_superuser)
    

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
