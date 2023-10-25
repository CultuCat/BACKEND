from rest_framework import serializers
from .models import Perfil
from spaces.serializers import SpaceSerializer

from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token


class PerfilSerializer(serializers.ModelSerializer):

    #trofeus = serializers.PrimaryKeyRelatedField(many=True, queryset=Trofeu.objects.all())
    #llocs_favorits = SpaceSerializer(many=True, read_only=True) 
    #amics = serializers.SlugRelatedField(many=True, slug_field='user', read_only=True)
    

    class Meta:
        model = Perfil
        fields = ('id','email','username', 'first_name','last_name', 'password', 'imatge','bio','puntuacio','isBlocked','wantsToTalk','isVisible','isAdmin')
        # 'trofeus', 'llocs_favorits', 'amics'
        
def checkCorrectLogin(data):
    user_act = data.get("user", None)
    if user_act is not None:
        username_act = user_act["username"]
        password_act = user_act["password"]
    else:
        username_act = data.get("username", None)
        password_act = data.get("password", None)

    try:
        user = Perfil.objects.get(username=username_act)
    except Perfil.DoesNotExist:
        raise serializers.ValidationError("No existeix un usuari amb aquest username.")

    if not user.is_active:
        raise serializers.ValidationError("Aquest usuari ha estat banejat o es troba pendent de confirmació.")

    pwd_valid = check_password(password_act, user.password)

    if not pwd_valid:
        raise serializers.ValidationError("Contrasenya incorrecta.")
    return user

def createLogin(data, user):
    token, created = Token.objects.get_or_create(user=user)
    data['token'] = token.key
    data['created'] = created
    return data
