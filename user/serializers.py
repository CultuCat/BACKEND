from rest_framework import serializers
from .models import Perfil

class PerfilSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = Perfil
        fields = ('id', 'username','password','email', 'first_name','is_staff','imatge', 'bio', 'puntuacio', 'isBlocked', 'wantsToTalk', 'isVisible')
