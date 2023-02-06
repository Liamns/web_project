from django.views.generic import TemplateView
from django.urls import path, include, re_path
from apis.views import LoginApi, LogoutApi, UserSignupView, ProfileUpdateView, UserPasswordResetConfirmView, UserPasswordResetCompleteView, UserPasswordResetDoneView, UserPasswordResetView,ProfileView
from event.views import ParticipatedEventView
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from allauth.account import views as allauth_views
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
router = DefaultRouter(trailing_slash=False)





urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    
    path('login/', TemplateView.as_view(template_name="user/login.html"), name="login"),
    path('jwt/login/', LoginApi.as_view(),name='jwt_login'),
    path('jwt/logout/', LogoutApi.as_view(),name='jwt_logout'),
    path('logout/', auth_views.LogoutView.as_view(template_name="home.html"),name="logout"),
    # 회원가입
    path("register/",  UserSignupView.as_view(), name="register"),

    # 이메일 관련 필요
    # 유효한 이메일이 유저에게 전달
    path('confirm-email/', allauth_views.email_verification_sent, name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', allauth_views.ConfirmEmailView.as_view(), name='account_confirm_email'),
    path("", include("allauth.urls")),
    path("password_reset/",
         UserPasswordResetView.as_view(),
         name="password_reset"),
    path(
        "password_reset/done/",
        UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    ### 프로필
    path("profile/<int:pk>/", ProfileView.as_view(), name='profile_view'),
    path("update/<int:pk>/", ProfileUpdateView.as_view(), name='profile_update'),
    path("profile/events/", ParticipatedEventView.as_view(), name='participated_event'),
]

