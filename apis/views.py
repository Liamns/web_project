from django.shortcuts import render
from user.models import User
from user.serializers import UserSerializer
from rest_framework.decorators import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime

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

    return res