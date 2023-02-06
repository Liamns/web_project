from rest_framework import  serializers
from .models import Event
from user.serializers import UserSerializer
from user.models import User

class EventImageSerializer(serializers.ModelSerializer):
    event_img = serializers.ImageField(use_url=True)

    class Meta:
        model = Event
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["user",'title', 'content', 'deadline', 'participants_limit', 'start_event', 'end_event', 'event_imgage', 'category', 'tags', 'location_tags']

class EventCreateSerializer(serializers.ModelSerializer):
    event_user = EventSerializer(many=True, )

    class Meta:
        model = User
        fields = ['id', 'event_user']


    def create(self, validated_data):
        events = validated_data.pop('event_user')
        user = User.objects.get(self.id)

        event= Event.objects.create(user_id=user, **event)
        return event