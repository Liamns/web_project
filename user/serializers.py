from rest_framework import serializers
from .models import User, Profile



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
        
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    profile_picture_id = serializers.IntegerField(
    write_only=True, required=False)
    message_count = serializers.SerializerMethodField("get_message_count")
    
    class Meta:
        model = Profile
        fields = "__all__"
        

    
class FavoriteSerializer(serializers.Serializer):
    favorite_id = serializers.IntegerField()