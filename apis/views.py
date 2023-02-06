from django.shortcuts import render, redirect, get_object_or_404
from user.models import User
from user.serializers import UserSerializer
from rest_framework import generics
from rest_framework.response import Response
import jwt,datetime
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework import status
from config import settings
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.decorators import APIView, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.urls import reverse_lazy

#수정사항
from rest_framework.permissions import AllowAny
from django.views.decorators.debug import sensitive_post_parameters

from allauth.account.views import SignupView
from user.forms import UserSignupForm

#회원가입
sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2'),
)

class UserSignupView(SignupView):
    """
    회원가입
    """
    template_name = "user/register.html"   
    form_class = UserSignupForm

@permission_classes([AllowAny])
@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        """
        email 과 password를 가지고 login 시도
        key값 : email, password
        """

        user = User
        email = request.data.get('email')
        password = request.data.get('password')
        
        if (email is None) or (password is None):
            return Response({
                "message": "email/password required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({
                "message": "유저를 찾을 수 없습니다"
            }, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({
                "message": "wrong password"
            }, status=status.HTTP_400_BAD_REQUEST)
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = Response(data={"message": "Success!!"},status=status.HTTP_200_OK, headers={"Authorization": access_token})

        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.set_cookie(key="access_token", value=access_token)

        return response

@permission_classes([AllowAny])
@method_decorator(csrf_protect, name='dispatch')
class RefreshJWTtoken(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refreshtoken')
        
        if refresh_token is None:
            return Response({
                "message": "Authentication credentials were not provided."
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256']
            )
        except:
            return Response({
                "message": "expired refresh token, please login again."
            }, status=status.HTTP_403_FORBIDDEN)
        
        user = User.objects.filter(id=payload['nkn']).first()
        
        if user is None:
            return Response({
                "message": "user not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({
                "message": "user is inactive"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = generate_access_token(user)
        response = Response(data={"message": "Success!!"},status=status.HTTP_200_OK, headers={"Authorization": access_token})

        response.set_cookie(key="access_token", value=access_token)
        
        return response
        
        
@method_decorator(csrf_protect, name='dispatch')
class LogoutApi(APIView):
    def post(self, request):
        """
        클라이언트 refreshtoken 쿠키를 삭제함으로 로그아웃처리
        """
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('refreshtoken')
        response.delete_cookie('access_token')
        response.delete_cookie('sessionid')
        return response

def generate_access_token(user):
    access_token_payload = {
        'nkn': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=0, minutes=30
        ),
        'iat': datetime.datetime.utcnow(),
    }
    
    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY, algorithm='HS256'
    )
    
    return access_token
    
    
def generate_refresh_token(user):
    refresh_token_payload = {
        'nkn': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    
    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.REFRESH_TOKEN_SECRET, algorithm='HS256'
    )
    
    return refresh_token


def jwt_login(response, user):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    
    data = {
        'access_token': access_token,
    }
    
    response.data = data
    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    return response



# 비밀번호 reset 담당 클래스 뷰
class UserPasswordResetView(PasswordResetView):
    # 이메일을 입력할 수 있는 화면
    template_name = "user/password_reset_form.html"
    # 이메일이 존재하는 경우 그 다음 작업을 진행할 경로 지정
    success_url = reverse_lazy("password_reset_done")
    # 이메일로 전송될 페이지 지정
    email_template_name = "user/password_reset_email.txt"

    def form_valid(self, form):
        # 사용자가 입력한 이메일이 실제 존재하는지 확인 후 없으면 에러 메세지 전송
        # 존재한다면 유효성 검증
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            messages.info(self.request, "이메일을 확인해주세요")
            return redirect("password_reset")


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "user/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "user/password_reset_confirm.html"


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "user/password_reset_complete.html"

### 프로필
class ProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile.html'

    def get(self, req, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)

        return Response({"user":user, "serializer":serializer})

# profile update
class ProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer