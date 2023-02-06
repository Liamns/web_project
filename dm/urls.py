
from django.contrib import admin
from django.urls import path, include


from . import views
from .views import ListThreads, CreateThread, ThreadView, CreateMessage,ThreadNotification


urlpatterns = [

    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/CreateMessage/', CreateMessage.as_view(), name='create-message'),
    
    path('notification/<int:notification_pk>/post/<int:post_pk>', ThreadNotification.as_view(), name='thread-notification'),
]
