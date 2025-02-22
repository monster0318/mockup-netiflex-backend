from rest_framework import serializers
from videoflix_app.models import Video
from user.api.serializers import UserSerializer


class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=150)
    author = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=1000,required=False)
    uploaded_by = UserSerializer(read_only=True)
    class Meta:
        model = Video
        fields = "__all__"
        read_only_fields = ['uploaded_at','updated_at']
      