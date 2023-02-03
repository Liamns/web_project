from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import APIView, permission_classes
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator

from .models import *

from config import settings
from apis.views import *
from apis.jwtdecoding import JWTDecoding
import jwt

# Create your views here.
class PostEventFormView(TemplateView):
    def get(self,req):
        return render(req, "event/events_form.html")

class PostEventDetailView(TemplateView):
    def get(self, req):
        return render(req, 'event/event_detail.html')

@permission_classes([AllowAny])       
class PostEventView(APIView):
    template_name = "event/event_list.html"
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, req):


        events = Event.objects.all()
        events_image = EventImage.objects.all()
        event_lens = len(EventImage.objects.all())


        return Response({"events" : events, "events_image":events_image, "event_lens":event_lens})


        


       
