
from django.urls import path
from django.views.generic import TemplateView
from django.urls import path, include


# ys
from apis.views import UserProfileView
from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

router.register("profile", UserProfileView)




urlpatterns = [
    path('rest_auth/', include('dj_rest_auth.urls')),
    path('rest_auth/register/', include('dj_rest_auth.registration.urls')),
    path('allauth/', include('allauth.urls')),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register")

]