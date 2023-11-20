from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    espai = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    enllacos_list = serializers.ListField(read_only=True, required=False, source='get_enllac')
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    class Meta:
        model = Event
        exclude = ['enllac', 'imatge']

    def get_espai(self, obj):
        return obj.espai_info

    def get_tags(self, obj):
        return obj.tags_info

class EventListSerializer(serializers.ModelSerializer):
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    espai = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'nom', 'descripcio', 'dataIni', 'imatges_list', 'espai', 'preu']

    def get_espai(self, obj):
        return obj.espai_info

class EventCreateSerializer(serializers.ModelSerializer):
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    
    class Meta:
        model = Event
        fields = '__all__'