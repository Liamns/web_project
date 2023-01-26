
from django.urls import path
from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework import routers


urlpatterns = [
    path('rest_auth/', include('dj_rest_auth.urls')),
    path('rest_auth/register/', include('dj_rest_auth.registration.urls')),
    path('allauth/', include('allauth.urls')),
    path("register/", TemplateView.as_view(template_name="user/register.html"), name="register"),
    path('login/', TemplateView.as_view(template_name="user/login.html"), name="login")

]