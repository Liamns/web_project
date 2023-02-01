from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # dose not return password in response json query
        extra_kwargs = {
    	    'password' : {'write_only' : True }
	    }

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
        #provide django, password will be hashing!
            instance.set_password(password)
        instance.save()
        return instance        

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