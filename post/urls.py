from django.urls import path
from .views import *

urlpatterns = [   
    # http://127.0.0.1:8000/post/
    path("", PostView.as_view(), name="post_home"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("detail/<int:pk>/", PostDetailView.as_view(), name="post_detail"),

]
