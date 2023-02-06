from django.urls import path
from .views import *
from django.urls import reverse_lazy

urlpatterns = [   
    # http://127.0.0.1:8000/post/
    path("", PostView.as_view(), name="post_home"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("detail/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/", detail, name="detail"),

]
