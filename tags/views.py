<<<<<<< Updated upstream
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tag
from .serializers import TagSerializer

class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
            return []
=======
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
>>>>>>> Stashed changes
