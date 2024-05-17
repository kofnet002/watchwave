from rest_framework import serializers
from .models import Video



class VideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_url', 'user', 'created_at', 'updated_at']

        # depth = 1