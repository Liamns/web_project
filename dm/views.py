from django.shortcuts import render, redirect

# Create your views here.
from .models import ThreadModel, MessageModel
from django.views import View
from django.db.models import Q

import jwt

# from django.contrib.auth.models import User
from user.models import User
from .forms import ThreadForm, MessageForm
from .models import MessageModel


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }
        return render(request, 'dm/inbox.html', context)
    
class CreateThread(View):
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

        try:
            receiver = User.objects.get(email=username)

            print(receiver)
            
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
        
class ThreadView(View):
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
    
    
class CreateMessage(View):
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
        return redirect('thread', pk=pk)