from rest_framework import serializers
from .models import Trophy
from message.models import Message
from comment.models import Comment
from ticket.models import Ticket
from user.models import FriendshipRequest
from discount.models import Discount

class TrophySerializer(serializers.ModelSerializer):
    level_achived_user = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Trophy
        fields = ['nom', 'descripcio', 'punts_nivell1', 'punts_nivell2', 'punts_nivell3', 'level_achived_user', 'progress']
        
    def get_level_achived_user(self, obj):
        user_id = self.context['request'].user.id
        ds = Discount.objects.filter(userDiscount=user_id, nomTrofeu=obj.nom)
        max = -1
        for d in ds:
            if d.nivellTrofeu > max:
                max = d.nivellTrofeu
        return max
    
    def get_progress(self, obj):
        user_id = self.context['request'].user.id
        prog = 0
        if obj.nom == "Xerraire":
            prog = Message.objects.filter(user_from = user_id).count()
        
        elif obj.nom == "Reviewer":
            prog = Comment.objects.filter(user = user_id).count()
            
        elif obj.nom == "Més esdeveniments":
            prog = Ticket.objects.filter(user = user_id).count()
        
        elif obj.nom == "El més amigable":
            prog = FriendshipRequest.objects.filter(from_user=user_id, is_accepted=True).count()+FriendshipRequest.objects.filter(to_user=user_id, is_accepted=True).count()
        
        elif obj.nom == "Coleccionista d'or":
            prog = Discount.objects.filter(nivellTrofeu=3, userDiscount=user_id).count()
          
        return prog
        
