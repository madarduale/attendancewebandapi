from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class TeacherAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = request.user
        if user.is_authenticated and user.is_teacher:
            return (user, None)
        raise AuthenticationFailed('Access denied')

class SuperuserAuthencication(BaseAuthentication):
    def authenticate(self, request):
        user = request.user
        if user.is_authenticated and user.is_superuser:
            return (user, None)
        raise AuthenticationFailed('Access denied')