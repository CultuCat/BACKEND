from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    imatges_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = ['user', 'event', 'imatges_list', 'image', 'pdf_url']
        
    def get_imatges_list(self, obj):
        return obj.event.get_imatge() if obj.event else None

class TicketSerializerByEvent(serializers.ModelSerializer):
    idUser = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = ['idUser', 'nickname', 'name', 'avatar']
        
    def get_idUser(self, obj):
        return obj.user.id if obj.user else None
    
    def get_nickname(self, obj):
        return obj.user.username if obj.user else None

    def get_name(self, obj):
        return obj.user.first_name if obj.user else None
    
    def get_avatar(self, obj):
        return obj.user.imatge if obj.user else None
        
def split_colon(obj):
        if obj:
            return obj.split(',')
        else:
            return None
        
class TicketSerializerByUser(serializers.ModelSerializer):
    nomEvent = serializers.SerializerMethodField()
    dataIni = serializers.SerializerMethodField()
    dataFi = serializers.SerializerMethodField()
    espai = serializers.SerializerMethodField()
    imatges_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = ['id', 'nomEvent', 'dataIni', 'dataFi', 'espai', 'imatges_list', 'image']
        
    def get_nomEvent(self, obj):
        return obj.event.nom if obj.event else None

    def get_dataIni(self, obj):
        return obj.event.dataIni if obj.event else None
    
    def get_dataFi(self, obj):
        return obj.event.dataFi if obj.event else None
    
    def get_espai(self, obj):
        return obj.event.espai.nom if obj.event else None
    
    def get_imatges_list(self, obj):
        return obj.event.get_imatge() if obj.event else None
    