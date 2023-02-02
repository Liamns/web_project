from django.urls import path
from .views import *
from django.urls import reverse_lazy

urlpatterns = [   
    # http://127.0.0.1:8000/post/
    path("", PostView.as_view(), name="post_main"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/", detail, name="detail"),

    # 이벤트 리스트 
    path("events/", PostEventView.as_view(), name="event_list"),

    # 이벤트 작성 폼
    # path("events/forms/", PostDetailView.as_view(), name="event_detail")
]
