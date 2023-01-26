from django.urls import path, include
<<<<<<< HEAD
from apis.views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('rest_auth/', include('dj_rest_auth.urls')),
    path('rest_auth/register/', include('dj_rest_auth.registration.urls')),
    path('allauth/', include('allauth.urls')),
    path('', include(router.urls))
=======



urlpatterns = [

>>>>>>> Song
]
