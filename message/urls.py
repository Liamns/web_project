from django.urls import path, include
from rest_framework import routers

from .views import GenericFileUploadView, MessageView
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

router = routers.DefaultRouter()
router.register('file-upload', GenericFileUploadView)
router.register('message', MessageView)



urlpatterns = [

    path('', include(router.urls))
    
]
