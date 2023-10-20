from rest_framework import generics, viewsets, status
from .models import Event
from .serializers import EventSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer