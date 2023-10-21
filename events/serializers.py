from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    enllacos_list = serializers.ListField(read_only=True, required=False, source='get_enllac')
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    
    class Meta:
        model = Event
        fields = '__all__'