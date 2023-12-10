from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
<<<<<<< Updated upstream
        fields = ('id', 'nom')
=======
        fields = ('nom')
>>>>>>> Stashed changes
