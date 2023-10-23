from rest_framework import serializers
from .models import Event
from comment.serializers import CommentSerializer

class EventSerializer(serializers.ModelSerializer):
    enllacos_list = serializers.ListField(read_only=True, required=False, source='get_enllac')
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    comments = CommentSerializer(many=True, read_only=True, source='comment_set') 
    class Meta:
        model = Event
        exclude = ['enllac', 'imatge']

class EventListSerializer(serializers.ModelSerializer):
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    
    class Meta:
        model = Event
        fields = ['id', 'nom', 'dataIni', 'imatges_list', 'espai', 'preu']