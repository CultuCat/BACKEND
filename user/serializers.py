from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil

from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token


class PerfilSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source = "user.email", read_only=True)
    username = serializers.CharField(source = "user.username", read_only=True)
    nom = serializers.CharField(source = "user.nom", read_only=True)
    password = serializers.CharField(source="user.password", required=False, write_only=True)

    class Meta:
        model = Perfil
        fields = ('user','email','username', 'nom', 'password', 'imatge','bio','puntuacio','isBlocked','wantsToTalk','isVisible')

        
def checkCorrectLogin(data):
    user_act = data.get("user", None)
    if user_act is not None:
        username_act = user_act["username"]
        password_act = user_act["password"]
    else:
        username_act = data.get("username", None)
        password_act = data.get("password", None)

    try:
        user = User.objects.get(username=username_act)
    except User.DoesNotExist:
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
