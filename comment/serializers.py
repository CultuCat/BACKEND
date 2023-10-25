from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        username = serializers.CharField(source="user.username", read_only=True)
        fields = '__all__'