from . import views
from django.urls import path
from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework import routers
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
    path('rest_auth/', include('dj_rest_auth.urls')),
    path('rest_auth/register/', include('dj_rest_auth.registration.urls')),
    path('allauth/', include('allauth.urls')),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
