from django.shortcuts import render
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse 

import requests
from user.models import User

import environ

env = environ.Env()
environ.Env.read_env()


@api_view(['POST'])
def Chat_engine(request, name):

    name = User.objects.filter(name=name)
    
    if name:
        
        response = requests.get('https://api.chatengine.io/users/me/', 
            headers={ 
                "Project-ID": env('CHAT_ENGINE_PROJECT_ID'),
                # "Private-Key": env('CHAT_ENGINE_PRIVATE_KEY'),
                "User-Name": name,
            }
        )
        return Response(response.json(), status=response.status_code)

    else:
        
        return HttpResponse('do not match back page plz')


