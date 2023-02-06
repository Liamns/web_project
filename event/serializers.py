from rest_framework import  serializers
from .models import Event

class EventImageSerializer(serializers.ModelSerializer):
    event_img = serializers.ImageField(use_url=True)

    class Meta:
        model = Event
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"