from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers 
from .models import * 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token
    
class MovieSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_img(self, obj):
        request = self.context.get('request')
        if obj.img and hasattr(obj.img, 'url'):
            img_url = obj.img.url
            return request.build_absolute_uri(img_url)
        else:
            return None


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat 
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment 
        fields = "__all__"




