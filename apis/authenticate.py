from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, CSRFCheck

from django.conf import settings
from django.contrib.auth import get_user_model
import jwt


User = get_user_model()


class SafeJWTAuthentication(BaseAuthentication):
    """
    JWT Authentication
    헤더의 jwt 값을 디코딩해 얻은 id 값을 통해서 유저 인증 여부를 판단한다.
    """
    
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        
        if not access_token:
            return None
            
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        
        return self.authenticate_credentials(request, payload['nkn'])
    
    def authenticate_credentials(self, request, key):
        user = User.objects.filter(id=key).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')
        
        self.enforce_csrf(request)
        return (user, None)

    def enforce_csrf(self, request):
        def dummy_get_response(request):
            return None

        check = CSRFCheck(dummy_get_response)
        
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')