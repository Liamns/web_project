from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Post,Comment,PostImage
from .forms import PostForm,CommentForm,PostImageForm
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

from post.serializers import PostSerializer

from config import settings
from apis.views import *
from apis.jwtdecoding import JWTDecoding
import jwt


@permission_classes([AllowAny])
@method_decorator(ensure_csrf_cookie, name="dispatch")
class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"
    permission_classes = [IsAuthenticated]


    def get(self, request):
        
        headers = request.COOKIES.get("access_token")
        
        if headers is None:
            return Response(data= {"login" : "로그인"},template_name="home.html")
        else:   
            try:
                payload = jwt.decode(headers, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=JWTDecoding.Jwt_decoding(request=request))
            except jwt.ExpiredSignatureError: # 토큰이 만료되었을 때 나오는 것
                return RefreshJWTtoken.post(request=request)
            except jwt.InvalidTokenError:
                raise Exception("Invalid token")

            if user is not None:
                response = Response({"user" : user}, template_name="home.html")

                

                    
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
    

def index(request):
    """
    post 전체 목록 추출(작성날짜 최신순)
    """

    #현재 페이지 번호
    page = request.GET.get('page',1)

    post_list = Post.objects.order_by("-created_at")

    paginator = Paginator(post_list, 10)
    page_obj = paginator.get_page(page)


    return render(request, "post/post_list.html",{"post_list":page_obj})

@login_required(login_url="login")
def detail(request, post_id):
    """
    post_id 에 맞는 질문 상세 추출
    """

    post = get_object_or_404(post, id=post_id)

    return render(request, "post/post_detail.html",{"post":post})

@login_required(login_url="login")
def post_create(request):
    """
    get: 비어 있는 폼, post : 바인딩 폼
    """
    if request.method == "POST":
        form = postForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = postForm()
    return render(request, "post/post_form.html",{"form":form})


@login_required(login_url="login")
def comment_create(request,post_id):
    """
    답변 등록 - get(비어 있는 폼) / post(바인딩 폼)
    """
    post = get_object_or_404(post, pk=post_id)

    # post.comment_set.create(content=request.POST['content'])
    # comment = comment(post=post, content=request.POST['content'])
    # comment.save()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("detail", post_id=post_id)
    else:
        form = CommentForm()

    return render(request,"post/post_detail.html",{"form":form,"post":post})


class PostEventView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "post/event_list.html"

    def get(self, req):
        post_serializer = PostSerializer()
        return Response({"post" : post_serializer})


"""
프로필 페이지 테스트
"""
def profile_view(request):
    return render(request, 'profile.html')
