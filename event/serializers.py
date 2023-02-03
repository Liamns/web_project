from rest_framework import  serializers
from .models import EventImage

class EventImageSerializer(serializers.ModelSerializer):
    event_img = serializers.ImageField(use_url=True)

    class Meta:
        model = EventImage
        fields = "__all__"