
from django.urls import path
from django.views.generic import TemplateView
from django.urls import path, include
from apis.views import LoginApi, LogoutApi, RegisterView


urlpatterns = [
    path('rest_auth/', include('dj_rest_auth.urls')),
    path('rest_auth/register/', include('dj_rest_auth.registration.urls')),
    path('allauth/', include('allauth.urls')),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register"),
    path('login/', LoginApi.as_view(), name='login'),
    path('logout/', LogoutApi.as_view(), name='logout'),
    path('registers/', RegisterView.as_view(), name='registers'),
]