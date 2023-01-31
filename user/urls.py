from . import views
from django.views.generic import TemplateView
from django.urls import path, include, re_path
from apis.views import LoginApi, LogoutApi, UserRegisterView, UserSignupView, ConfirmEmailView, google_callback, google_login, GoogleLogin
from dj_rest_auth.registration.views import VerifyEmailView


urlpatterns = [
    path("register/", TemplateView.as_view(template_name="user/register.html"), name="register"),
    path('login/', TemplateView.as_view(template_name="user/login.html"), name="login"),
    path('jwt/login/', LoginApi.as_view(),name='jwt_login'),
    path('jwt/logout/', LogoutApi.as_view(),name='jwt_logout'),
    # path('jwt/register/', UserSignupView.as_view(),name='jwt_register'),

    path("jwt/register/",  UserSignupView.as_view(), name="register"),

    # 이메일 관련 필요
    path('accounts/allauth/', include('allauth.urls')),
    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    # JWT Social
    path('google/login', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),  
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    # JWT Social
]

