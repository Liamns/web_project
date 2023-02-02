from django.shortcuts import render, redirect
from user.models import User, Profile
from user.serializers import UserSerializer, ProfileSerializer
from rest_framework.decorators import APIView
from rest_framework.response import Response

import jwt,datetime


from rest_framework import status
from django.conf import settings
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



#회원가입

@permission_classes([AllowAny])
@method_decorator(ensure_csrf_cookie, name="dispatch")
class RegisterView(APIView) :

    def post(self, req):
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

User = get_user_model()


#로그인

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
        
        response = Response(status=status.HTTP_200_OK)
        return jwt_login(response, user)
        

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
        
@permission_classes([AllowAny])
@method_decorator(ensure_csrf_cookie, name="dispatch")
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
        'nkn': user.nickname,
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
        'nkn': user.nickname,
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