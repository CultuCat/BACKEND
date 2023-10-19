from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Space
from .serializers import SpaceSerializer

class SpaceListCreateView(generics.ListCreateAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer