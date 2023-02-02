from django.urls import path
from .views import *
from django.urls import reverse_lazy

urlpatterns = [   

    # 이벤트 리스트 
    path("", PostEventView.as_view(), name="event_list"),

    # 이벤트 작성 폼
    path("forms/", PostEventFormView.as_view(), name="event_detail"),

    # 이벤트 디데일 뷰
    path("detail/", PostEventDetailView.as_view(), name="event_detail")

]
