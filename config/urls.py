"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView, 
    TokenRefreshSlidingView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import re_path
from . import views


from post.views import HomeView
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path('user/', include('dj_rest_auth.urls')),
    path('user/', include('allauth.urls')),
    path('user/', include('user.urls')),
    path('post/', include('post.urls')),
    path('events/', include('event.urls')),

    path('chat2/', include('chat2.urls')),
    path('dm/', include('dm.urls')),
    
    path('profile/', profile_view, name='profile'),
    path('profile_edit/', profile_edit_view, name='profile'),

    
    path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('schedule/', TemplateView.as_view(template_name = "schedule.html"), name='schedule'),
    
    re_path('login', views.login),
    re_path('signup', views.signup),
    
    
]

urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
