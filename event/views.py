from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core import serializers
from rest_framework.decorators import api_view

from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpRequest, HttpResponse, Http404
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
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from datetime import datetime
from django.utils.dateformat import DateFormat

class EventPagination(CursorPagination):
    page_size = 8


# Create your views here.
class PostEventFormView(TemplateView):
    def get(self,req):
        return render(req, "event/events_form.html")

class PostEventDetailView(TemplateView):
    def get(self, req):
        return render(req, 'event/event_detail.html')

@permission_classes([AllowAny])       
class PostEventView(TemplateView):
    template_name = "event/event_list.html"


    def get(self, req):
        event_list = Event.objects.all()

        page = req.GET.get('page', 1)
        paginator = Paginator(event_list, 4)

        now = DateFormat(datetime.now())


        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)
            
            

        return render(req, "event/event_list.html",{"events" : events, "event_list" : event_list})
        


        #     def get(self, req):

        

        
        # page = int(req.GET.get("page"))

        # limit = 8
        # offset = limit * (page - 1)

            

        # if offset == 0:
        #     events = Event.objects.all()[offset : offset + limit]
        #     return render(req, "event/event_list.html",{"events" : events})
        

        # events = Event.objects.all()[offset : offset + limit]
        # data = serializers.serialize("json", list(events))
        # return HttpResponse(json.dumps(data), content_type="application/json")



        


       
