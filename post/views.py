from django.shortcuts import render,redirect, get_object_or_404
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
    template_name = "post/post_main.html"

class PostCreateView(TemplateView):
    template_name = "post/post_create.html"

class PostDetailView(TemplateView):
    template_name = "post/post_detail.html"
    

def index(request):
    """
    Post 전체 추출(작성날짜 최신순)
    """ 

    # 주소 정리
    address_total = [
    {"서울":["종로구","중구","용산구","성동구","광진구","동대문구","중랑구","성북구","강북구","도봉구","노원구","은평구","서대문구","마포구","양천구","강서구","구로구","금천구","영등포구","동작구","관악구","서초구","강남구","송파구","강동구"]}, 
    {"경기":["수원시","성남시","의정부시","안양시","부천시","광명시","동두천시","평택시","안산시","고양시","과천시","구리시","남양주시","오산시","시흥시","군포시","의왕시","하남시","용인시","파주시","이천시","안성시","김포시","화성시","광주시","양주시","포천시","여주시","연천군","가평군","양평군"]}, 
    {"인천":["중구","동구","미추홀구","연수구","남동구","부평구","계양구","서구","강화군","옹진군"]}, 
    {"강원":["춘천시","원주시","강릉시","동해시","태백시","속초시","삼척시","홍천군","횡성군","영월군","평창군","정선군","철원군","화천군","양구군","인제군","고성군","양양군"]}, 
    {"충북":["청주시","충주시","제천시","보은군","옥천군","영동군","증평군","진천군","괴산군","음성군","단양군"]}, 
    {"충남":["천안시","공주시","보령시","아산시","서산시","논산시","계룡시","당진시","금산군","부여군","서천군","청양군","홍성군","예산군","태안군"]}, 
    {"대전":["동구","중구","서구","유성구","대덕구"]},
    {"세종특별자치시":["조치원읍","연기면","연동면","부강면","금남면","장군면","연서면","전의면","전동면","소정면","한솔동","도담동","아름동","종촌종","고운동","보람동","새롬동","대평동","소담동","다정동","해밀동","반곡동"]}, 
    {"전북":["전주시","군산시","익산시","정읍시","남원시","김제시","완주군","진안군","무주군","장수군","임실군","순창군","고창군","부안군"]}, 
    {"전남":["목포시","여수시","순천시","나주시","광양시","담양군","곡성군","구례군","고흥군","보성군","화순군","장흥군","강진군","해남군","영암군","무안군","함평군","영광군","장성군","완도군","진도군","신안군"]}, 
    {"광주":["동구","서구","남구","북구","광산구"]}, 
    {"경북":["포항시","경주시","김천시","안동시","구미시","영주시","영천시","상주시","문경시","경산시","군위군","의성군","청송군","영양군","영덕군","청도군","고령군","성주군","칠곡군","예천군","봉화군","울진군","울릉군"]}, 
    {"대구":["중구","동구","서구","남구","북구","수성구","달서구","달성군"]}, 
    {"울산":["중구","남구","동구","북구","울주군"]}, 
    {"경남":["창원시","진해구","진주시","통영시","사천시","김해시","밀양시","거제시","양산시","의령군","함안군","창녕군","고성군","남해군","하동군","산청군","함양군","거창군","합천군"]}, 
    {"부산":["중구","서구","동구","영도구","부산진구","동래구","남구","북구","강서구","해운대구","사하구","금정구","연제구","수영구","사상구"]}, 
    {"제주":["제주시","서귀포시"]}
    ]

    # 검색어 받기
    keyword = request.GET.get('keyword','')

    # 정렬 기준 받기
    so = request.GET.get('so','latest') # sort 기준 : latest(기본)

    # 주소 가져오기
    address = request.GET.get('address', '')

    # 전체 게시물 추출
    if so == "latest":
        all_posts = Post.objects.order_by('-created_at')
    elif so == "inquiry":
        all_posts = Post.objects.annotate(num_answer=Count('view_cnt')).order_by('-view_cnt','-created_at')

    # 전체 리스트에서 검색어가 들어간 리스트만 추출(질문 제목, 질문 내용)
    # Q : OR 조건으로 데이터 조회, distinct() : 중복 제거
    if keyword:
        all_posts = all_posts.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword)).distinct()
    if address:
        all_posts = all_posts.filter(Q(location_tags__icontains=address))
    return render(request, 'post/post_main.html', {"address":address, "keyword":keyword, "so":so})

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