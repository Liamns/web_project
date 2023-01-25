from django.shortcuts import render
from user.models import User
from message.serializers import UserSerializer
from rest_framework.decorators import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer