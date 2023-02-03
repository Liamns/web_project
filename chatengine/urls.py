
from django.contrib import admin
from django.urls import path, include


from . import views


urlpatterns = [

    path('', views.Chat_engine, name='Chat_engine'),

]
