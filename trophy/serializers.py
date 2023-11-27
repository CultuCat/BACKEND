from rest_framework import serializers
from .models import Trophy
from discount.models import Discount

class TrophySerializer(serializers.ModelSerializer):
    level_achived_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Trophy
        fields = ['nom', 'descripcio', 'punts_nivell1', 'punts_nivell2', 'punts_nivell3', 'level_achived_user']
        
    def get_level_achived_user(self, obj):
        user_id = self.context['request'].user.id
        ds = Discount.objects.filter(userDiscount=user_id, nomTrofeu=obj.nom)
        max = -1
        for d in ds:
            if d.nivellTrofeu > max:
                max = d.nivellTrofeu
        return max
