from django.shortcuts import render,redirect, get_object_or_404, resolve_url
from django.views.generic.base import TemplateView
from .models import Post,Comment
from .forms import PostForm,CommentForm
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

from django.db.models import Q, Count

@permission_classes([AllowAny])
@method_decorator(ensure_csrf_cookie, name="dispatch")
class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"


    def get(self, request):
        
        headers = request.COOKIES.get("access_token")
        
        if headers is None:
            return Response(data= {"login" : "로그인"},template_name="home.html")
        else:   
            try:
                payload = jwt.decode(headers, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=JWTDecoding.Jwt_decoding(request=request))
            except jwt.ExpiredSignatureError: # 토큰이 만료되었을 때 나오는 것
                return RefreshJWTtoken.post(self, request=request)
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
    


class PostCreateView(TemplateView):
    template_name = "post/post_create.html"

class PostDetailView(TemplateView):
    template_name = "post/post_detail.html"
    
class PostView(TemplateView):
    template_name = "post/post_main.html"

    def get(self, request):
        """
        Post 전체 추출(작성날짜 최신순)
        """ 

        # 검색어 받기
        keyword = request.GET.get('keyword','')

        # 정렬 기준 받기
        so = request.GET.get('so','latest') # sort 기준 : latest(기본)

        # 주소 가져오기
        address = request.GET.get('address', '')

        # 어떤 모임 가져오기
        gathering = request.GET.get('gathering', '')

        # 전체 게시물 추출
        if so == "latest":
            all_posts = Post.objects.order_by('-created_at')
        elif so == "inquiry":
            all_posts = Post.objects.annotate(num_answer=Count('view_cnt')).order_by('view_cnt','-created_at')

        # 전체 리스트에서 검색어가 들어간 리스트만 추출(질문 제목, 질문 내용)
        # Q : OR 조건으로 데이터 조회, distinct() : 중복 제거
        if address == "전체":
            all_posts = Post.objects.order_by('-created_at')
        
        else:
            all_posts = all_posts.filter(Q(location_tags__icontains=address))
            
        if gathering:
            all_posts = all_posts.filter(Q(category__icontains=gathering))

        if keyword:
            all_posts = all_posts.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword)).distinct()
        return render(request, 'post/post_main.html', {"address":address, "gathering":gathering, "keyword":keyword, "so":so, "all_posts":all_posts})

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


class PostEventView(TemplateView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "post/event_list.html"

    def get(self, req):
        post_serializer = PostSerializer()
        return render(req, "post/event_list.html")
        
def profile_view(request):
    return render(request, 'profile.html')

def profile_edit_view(request):
    return render(request, 'profile-edit.html')