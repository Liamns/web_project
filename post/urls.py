from django.urls import path
from . import views
from django.urls import reverse_lazy

urlpatterns = [   
    # http://127.0.0.1:8000/post
    path("", views.PostView.as_view(), name="post"),
    path("create/", views.post_create, name="post_create"),
    path("<int:pk>/", views.detail, name="detail"),

]
