from rest_framework import generics, viewsets, status
from .models import Event
from .serializers import EventSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        event = request.data.copy()
        # Per asegurar-se que l'id no es repeteix, agafarem el mes antic i li restarem 1
        id = Event.objects.all().order_by('id').first().id - 1
        event['id'] = id
        serializer = self.get_serializer(data=event)
        #serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
