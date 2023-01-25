from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from .serializers import GenericFileUpload, GenericFileUploadSerializer, Message, MessageAttachment, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



class GenericFileUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serializer_class = GenericFileUploadSerializer
    

class MessageView(ModelViewSet):
    queryset = Message.objects.select_related(
        'sender', 'receiver').prefetch_related('message_attachments')
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, )
    
    def create(self, request, *args, **kwargs):
        
        attachments = request.data.pop('attachments', None)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if attachments:
            MessageAttachment.objects.bulk_create([MessageAttachment(
                **attachment, message_id=serializer.data['id']) for attachment in attachments])
        
        return Response(serializer.data, status=201)