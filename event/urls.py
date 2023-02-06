from django.urls import path
from .views import *
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [   

    # 이벤트 리스트 
    path("", PostEventView.as_view(), name="event_list"),

    # 이벤트 작성 폼
    path("forms/", PostEventFormView.as_view(), name="event_form"),

    # 이벤트 디데일 뷰
    path("<int:pk>/detail/", PostEventDetailView.as_view(), name="event_detail")

]
