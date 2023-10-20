from rest_framework import serializers

from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = "user.nickname", read_only=True)
    password = serializers.CharField(source="user.password", required=False, write_only=True)

    class Meta:
        model = Perfil
        fields = ('name', 'nickname', 'password', 'imatge', 'puntuacio')
