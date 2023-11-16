from rest_framework import serializers
from .models import Ticket
from events.models import Event

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class TicketSerializer_byEvent(serializers.ModelSerializer):
    nickname = serializers.CharField(default="user1")
    name = serializers.CharField(default="Carla Sabater")
    avatar = serializers.CharField(default="https://randomuser.me/api/portraits/women/1.jpg")
    
    class Meta:
        model = Ticket
        fields = ['nickname', 'name', 'avatar']
    
    # nickname = serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    # avatar = serializers.SerializerMethodField()
    
    # class Meta:
    #     model = Ticket
    #     fields = ['nickname', 'name', 'avatar']
        
    # def get_nickname(self, obj):
    #     return obj.user.username if obj.user else None

    # def get_name(self, obj):
    #     return obj.user.username if obj.user else None
    
    # def get_avatar(self, obj):
    #     return obj.user.username if obj.user else None
        
class TicketSerializer_byUser(serializers.ModelSerializer):
    #eventObj = Event.objects.filter(id=self.event)
    nomEvent = serializers.SerializerMethodField()#serializers.CharField(default=eventObj.nom)
    data = serializers.SerializerMethodField()#serializers.CharField(default=eventObj.dataIni)
    #url = serializers.CharField(default=eventObj.enllac)
    #imatge = serializers.CharField(default="/portraits/women/1.jpg")
    
    class Meta:
        model = Ticket
        fields = ['nomEvent', 'data'] #, 'url', 'imatge'
        
    def get_nomEvent(self, obj):
        return obj.event.nom if obj.event else None

    def get_data(self, obj):
        return obj.event.dataIni if obj.event else None