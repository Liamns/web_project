from django.shortcuts import render, redirect

# Create your views here.

from chat2.models import Message, Room
from django.http import HttpResponse, JsonResponse


def home(request):
    return render(request, 'chat2/home.html')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    
    return render(request, 'chat2/room.html', {'username':username, 'room':room, 'room_details': room_details})

def checkview(request):

    room = request.POST['room_name'] 
    username = request.POST['username'] 
    
    print(room, ", ", username)

    if Room.objects.filter(name=room).exists():
        return redirect('/chat2/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        #  path('<str:room>/', views.room, name='room')
        return redirect('/chat2/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    
    
    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    
    return HttpResponse('Message snet successfully')


def getMessages(request, room):
    
    room_details = Room.objects.get(name=room)
    
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({'messages':list(messages.values())})
