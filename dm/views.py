from django.shortcuts import render, redirect

# Create your views here.
from .models import ThreadModel, MessageModel
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

import jwt

# from django.contrib.auth.models import User
from user.models import User, Profile
from .forms import ThreadForm, MessageForm
from .models import MessageModel, Notification

@ permission_classes([IsAuthenticated])
class ThreadNotification(APIView):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)
        
        notification.user_has_seen = True
        notification.save()
        
        return redirect('thread', pk=object_pk)


@ permission_classes([IsAuthenticated])
class ListThreads(APIView):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        print(threads)
        context = {
            'threads': threads
        }
        return render(request, 'dm/inbox.html', context)
    
@ permission_classes([IsAuthenticated])
class CreateThread(APIView):
    def get(self, request, *args, **kwargs):
        
        form = ThreadForm()

        context = {
            'form': form
        }
        return render(request, 'dm/create-thread.html', context)


    def post(self, request, *args, **kwargs):
        
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        
        print("create post")
        print(username)

        try:
            receiver = User.objects.get(email=username)

            print(receiver)
            print(request.user)
            
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                print(thread)
                return redirect('thread', pk=thread.pk)
            
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')
        
@ permission_classes([IsAuthenticated])        
class ThreadView(APIView):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'dm/thread.html', context)
    
@ permission_classes([IsAuthenticated])
class CreateMessage(APIView):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()
        
        notification = Notification.objects.create(
            notification_type=4,
            from_user=request.user,
            to_user=receiver,
            thread=thread
            
        )
        
        return redirect('thread', pk=pk)