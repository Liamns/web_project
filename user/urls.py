from . import views
from django.views.generic import TemplateView
from django.urls import path, include, re_path
from apis.views import LoginApi, LogoutApi, RegisterView, ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)






urlpatterns = [
    path('rest_auth/', include('dj_rest_auth.urls')),
    path('rest_auth/register/', include('dj_rest_auth.registration.urls')),
    path('allauth/', include('allauth.urls')),
    path("register/", TemplateView.as_view(template_name="user/register.html"), name="register"),
    path('login/', TemplateView.as_view(template_name="user/login.html"), name="login"),
    path('jwt/login/', LoginApi.as_view(),name='jwt_login'),
    path('jwt/logout/', LogoutApi.as_view(),name='jwt_logout'),
    path('jwt/register/', RegisterView.as_view(),name='jwt_register'),
    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]

