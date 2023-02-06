from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["user","title", "content", "post_img", "category", "tags", "location_tags"]
        model = Post
