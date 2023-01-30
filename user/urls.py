from . import views
from django.urls import path
from django.views.generic import TemplateView
from django.urls import path, include
from apis.views import LoginApi, LogoutApi, RegisterView, Activate


urlpatterns = [
    path('rest_auth/', include('dj_rest_auth.urls')),
    path('rest_auth/register/', include('dj_rest_auth.registration.urls')),
    path('allauth/', include('allauth.urls')),
    path("register/", TemplateView.as_view(template_name="user/register.html"), name="register"),
    path('activate/<str:uidb64>/<str:token>/', Activate.as_view()), # 회원가입 시 이메일 인증 url
    path('login/', TemplateView.as_view(template_name="user/login.html"), name="login"),
    path('jwt/login/', LoginApi.as_view(),name='jwt_login'),
    path('jwt/logout/', LogoutApi.as_view(),name='jwt_logout'),
    path('jwt/register/', RegisterView.as_view(),name='jwt_register'),
]

