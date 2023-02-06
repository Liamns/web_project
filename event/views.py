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
from event.models import Event, Participants
from user.serializers import UserSerializer
from event.serializers import EventSerializer
from .serializers import EventSerializer

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

class PostEventFormView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "event/events_form.html"

    def get(self,req):
        return render(req, "event/events_form.html")

    def post(self, req):

        user = User.objects.get(id=JWTDecoding.Jwt_decoding(request=req))

        post_event = EventSerializer(data=req.data)
    # 장고와 달리 DRF에서는 request에서 데이터를 받을 때(request.data)
    # 반드시 .is_valid() 여부를 체크해야 한다.
    # valid하지 않을 때는 serializer.errors를 리턴한다.
        if post_event.is_valid():
            # event = EventSerializer(data=post_event["event_user"])
            # if event.is_valid():
            post_event.save()
            return HttpResponse(post_event.data, status = status.HTTP_201_CREATED)
        return HttpResponse(post_event.errors, status = status.HTTP_400_BAD_REQUEST)

class PostEventDetailView(TemplateView):
    def get(self, req, pk):
        event = get_object_or_404(Event, pk=pk)
        return render(req, 'event/event_detail.html', {"event" : event})

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
            
            

        return render(req, "event/event_list.html",{"events" : events})
        


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


class ParticipatedEventView(APIView):
    def post(self, req, pk):
        user = get_object_or_404(User, pk=pk)
        events = Event.objects.filter(user=user)

        return Response({"events":events})