from rest_framework import serializers
from .models import Trophy

class TrophySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trophy
        fields = '__all__'
