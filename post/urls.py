from django.urls import path
from . import views
from django.urls import reverse_lazy

from . import views

urlpatterns = [   

    # http://127.0.0.1:8000/contents/
    
    # 컨텐츠 홈    
    path("", views.PostView.as_view(), name="post"),
]
