from django.shortcuts import render, redirect
from user.models import User, Profile
from user.serializers import UserSerializer, ProfileSerializer
from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

import jwt,datetime


from rest_framework import status
from config import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.decorators import APIView, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

#ys
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q, Count, Subquery, OuterRef
import re


#수정사항
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import APIView, permission_classes
from django.http import HttpResponseRedirect

from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.utils import import_callable
from django.views.decorators.debug import sensitive_post_parameters

from allauth.account.views import SignupView
from user.forms import UserSignupForm
from allauth.utils import get_request_param
from allauth.account.utils import passthrough_next_redirect_url
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

# 프로필 View
class UserProfileView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = (IsAuthenticatedCustom, )

    def get_queryset(self): 
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        if keyword:
            search_fields = (
                "user__name", "profile_img", "user__email"
            )
            query = self.get_query(keyword, search_fields)
            try:
                return self.queryset.filter(query).filter(**data).exclude(
                    Q(user_id=self.request.user.id) |
                    Q(user__is_superuser=True)
                ).annotate(
                    fav_count=Count(self.user_fav_query(self.request.user))
                ).order_by("-fav_count")
            except Exception as e:
                raise Exception(e)

        result = self.queryset.filter(**data).exclude(
            Q(user_id=self.request.user.id) |
            Q(user__is_superuser=True)
        ).annotate(
            fav_count=Count(self.user_fav_query(self.request.user))
        ).order_by("-fav_count")
        return result

    @staticmethod
    def user_fav_query(user):
        try:
            return user.user_favorites.favorite.filter(id=OuterRef("user_id")).values("pk")
        except Exception:
            return []


    @staticmethod

    def get_query(query_string, search_fields):
      
        ''' Returns a query, that is a combination of Q objects. that combination
        aims to search keywords within a model by testion the give search fields.
        '''
      
      
        query = None  # Query to search for every search term
        terms = UserProfileView.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
      ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
          and grouping quoted words together
          
          Examlple:
          >>> normalize_query(some random words with quotes and spaces)
          ['some','random','words','with','quotes','and','spaces']
      '''
      return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

#회원가입

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2'),
)

@permission_classes([AllowAny])
class UserRegisterView(RegisterView) :

    serializers = getattr(settings, 'REST_AUTH_REGISTER_SERIALIZERS', {})

    RegisterSerializer = import_callable(serializers.get('REGISTER_SERIALIZER', UserSerializer))

    permission_classes = [AllowAny]

    def get(self, req):
        user = UserSerializer()
        return Response({"user" : user}, template_name="user/register.html")

class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect('/') # 인증성공

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/') # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

class UserSignupView(SignupView):
    template_name = "user/register.html"
    success_url = "home.html"
    redirect_field_name = "home.html"
    form_class = UserSignupForm

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        form = ret["form"]
        email = self.request.session.get("account_verified_email")
        if email:
            email_keys = ["email"]
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(
            self.request, reverse("home"), self.redirect_field_name
        )
        redirect_field_name = self.redirect_field_name
        site = get_current_site(self.request)
        redirect_field_value = get_request_param(self.request, redirect_field_name)
        ret.update(
            {
                "login_url": login_url,
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": redirect_field_value,
                "site": site,
            }
        )
        return ret
    
    


User = get_user_model()

@permission_classes([AllowAny])
@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        """
        email 과 password를 가지고 login 시도
        key값 : email, password
        """

        user = User
        email = request.data.get('email')
        password = request.data.get('password')
        
        if (email is None) or (password is None):
            return Response({
                "message": "email/password required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({
                "message": "유저를 찾을 수 없습니다"
            }, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({
                "message": "wrong password"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = Response(data={"message": "Success!!"},status=status.HTTP_200_OK, headers={"Authorization": access_token})        
        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.set_cookie(key="access_token", value=access_token)

        return response


@method_decorator(csrf_protect, name='dispatch')
class RefreshJWTtoken(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refreshtoken')
        
        if refresh_token is None:
            return Response({
                "message": "Authentication credentials were not provided."
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256']
            )
        except:
            return Response({
                "message": "expired refresh token, please login again."
            }, status=status.HTTP_403_FORBIDDEN)
        
        user = User.objects.filter(id=payload['nkn']).first()
        
        if user is None:
            return Response({
                "message": "user not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({
                "message": "user is inactive"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = generate_access_token(user)
        
        return Response(
            {
                'access_token': access_token,
            }
        )
        
        
@method_decorator(csrf_protect, name='dispatch')
class LogoutApi(APIView):
    def post(self, request):
        """
        클라이언트 refreshtoken 쿠키를 삭제함으로 로그아웃처리
        """
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('refreshtoken')

        return response

def generate_access_token(user):
    access_token_payload = {
        'nkn': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=0, minutes=30
        ),
        'iat': datetime.datetime.utcnow(),
    }
    
    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY, algorithm='HS256'
    )
    
    return access_token
    
    
def generate_refresh_token(user):
    refresh_token_payload = {
        'nkn': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    
    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.REFRESH_TOKEN_SECRET, algorithm='HS256'
    )
    
    return refresh_token


def jwt_login(response, user):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    
    data = {
        'access_token': access_token,
    }
    
    response.data = data
    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)

    return response
