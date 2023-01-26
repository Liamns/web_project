from django.shortcuts import render
from user.models import User, Profile
from user.serializers import UserSerializer, ProfileSerializer
from rest_framework.decorators import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime

#ys
from chat.custom_methods import IsAuthenticatedCustom
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q, Count, Subquery, OuterRef
import re


# 회원가입 DRF View
class RegisterView(APIView) :
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# 로그인 DRF View
class LoginView(APIView):
  def post(self,req):
    email = req.data['email']
    password = req.data['password']

    # email is unique,
    user = User.objects.filter(email=email)
    serialize_user = UserSerializer(user)
    json_user = JSONRenderer().render(serialize_user.data)

    if user is None :
      raise AuthenticationFailed('User does not found!')

    # is same?
    if not user.check_password(password) :
      raise AuthenticationFailed("Incorrect password!")
	
    ## JWT 구현 부분
    payload = {
      'ids' : user.id,
      'exp' : datetime.datetime.now() + datetime.timedelta(minutes=60),
      'iat' : datetime.datetime.now()
      }

    token = jwt.encode(payload,"secretJWTkey",algorithm="HS256")

    res = Response()
    res.set_cookie(key='jwt', value=token, httponly=True)
    res.data = {
        'jwt' : token
      }


    return res


# 로그인 여부 확인 View
class UserView(APIView) :
  def get(self,req):
    token = req.COOKIES.get('jwt')

    if not token :
      raise AuthenticationFailed('UnAuthenticated!')

    try :
      payload = jwt.decode(token,'secretJWTkey',algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('UnAuthenticated!')

    user = User.objects.filter(id=payload['id'])
    serializer = UserSerializer(user)

    return Response(serializer.data)

# 로그아웃 View
class LogoutView(APIView) :
  def post(self,req):
    res = Response()
    res.delete_cookie('jwt')
    res.data = {
        "message" : 'success' 
      }

    return 
  
# 프로필 View
class UserProfileView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedCustom, )

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