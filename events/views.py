from rest_framework import generics, viewsets, status
from .models import Event
from spaces.models import Space
from tags.models import Tag
from .serializers import EventSerializer, EventListSerializer, EventCreateSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.permissions import IsAdmin
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    models = Event
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    ordering_fields = ['dataIni']

    filterset_fields = ['espai']

    apply_permissions = False

    def get_permissions(self):
        if self.action == 'create' and self.apply_permissions:
            return [IsAdmin()]
        else:
            return []

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == 'create':    
            return EventCreateSerializer
        return EventSerializer

    def create(self, request, *args, **kwargs):
        event_data = request.data.copy()

        # Per asegurar-se que l'id no es repeteix, agafarem el mes antic i li restarem 1
        last_event = Event.objects.all().order_by('id').first()
        if last_event:
            id = last_event.id - 1
        else:
            id = 99999999999
        event_data['id'] = id

        event = Event.create_event(event_data)

        serializer = self.get_serializer(event)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
