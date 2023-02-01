
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

app_name = 'chat'

urlpatterns = [
    path("", views.index, name="index"),
    re_path("<str:room_name>/", views.room, name="room"),
]  