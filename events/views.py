from rest_framework import generics, viewsets, status
from .models import Event
from spaces.models import Space
from .serializers import EventSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.permissions import IsAdmin
from rest_framework.pagination import PageNumberPagination

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    models = Event
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        event = request.data.copy()
        # Per asegurar-se que l'id no es repeteix, agafarem el mes antic i li restarem 1
        last_event = Event.objects.all().order_by('id').first()
        if last_event:
            id = last_event.id - 1
        else:
            id = 99999999999
        event['id'] = id
        Space.get_or_create(nom = event['espai'], latitud = event['latitud'], longitud = event['longitud'])
        serializer = self.get_serializer(data=event)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
