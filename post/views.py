from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import APIView, permission_classes
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator

from post.serializers import PostSerializer

from config import settings
from apis.authenticate import *
import jwt


@permission_classes([AllowAny])
@method_decorator(ensure_csrf_cookie, name="dispatch")
class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"
    permission_classes = [IsAuthenticated]


    def get(self, request):
        
        headers = request.COOKIES.get("access_token")
        if headers == None:
            return Response(template_name="home.html")
        
        

        try:
            payload = jwt.decode(headers, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['nkn'])
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

        response = Response({"user" : user}, template_name="home.html")
        response.set_cookie(key="access_token", value=headers)

                
        return response

    # def dispatch(self, request, *args, **kwargs):
    #     """
    #     client 요청이 들어왔을 때 로그인 정보가 있다면 contents 이동 
    #     없다면 원래대로 home
    #     """
    #     if not request.user.is_anonymous:
    #         return redirect("post")

    #     return super().dispatch(request, *args, **kwargs)
    

class PostView(TemplateView):
    template_name = "post/main.html"


class PostEventView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "post/event_list.html"

    def get(self, req):
        post_serializer = PostSerializer()
        return Response({"post" : post_serializer})